import dlib
import cv2
import numpy as np
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from collections import namedtuple

Borders = namedtuple('Borders', 'left top right bottom')


class NoFacesError(Exception):
    pass


class MultiplyFacesError(Exception):
    pass


def get_square_borders(image_width, image_height):
    if image_width == image_height:
        return Borders(left=0, top=0, right=image_width, bottom=image_height)

    diff = abs(image_width - image_height)

    if image_width > image_height:
        left = diff / 2
        right = image_width - diff / 2
        upper = 0
        lower = image_height
    else:
        left = 0
        right = image_width
        upper = diff / 2
        lower = image_height - diff / 2

    return Borders(left=left, top=upper, right=right, bottom=lower)


def get_cv2_image(img):
    if isinstance(img, InMemoryUploadedFile):
        img_data = img.read()
        nparr = np.frombuffer(img_data, np.uint8)
        cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    elif isinstance(img, Image.Image):
        img = img.convert('RGB')
        cv2_image = np.array(img)
    else:
        raise TypeError('ожидается файл изображения')

    return cv2_image


def find_face(img):
    cv2_image = get_cv2_image(img=img)

    # Инициализация детектора лиц с использованием модели HOG
    face_detector = dlib.get_frontal_face_detector()

    # Обнаружение лиц на изображении
    faces = face_detector(cv2_image, 1)
    if not faces:
        raise NoFacesError('Лиц не обнаружено')
    if len(faces) > 1:
        raise MultiplyFacesError('Много лиц')
    else:
        return faces[0]


def get_face_borders(face):
    # Получение координат прямоугольной области первого обнаруженного лица
    left = face.left()
    top = face.top()
    right = face.right()
    bottom = face.bottom()
    return Borders(left=left, top=top, right=right, bottom=bottom)


def get_image_to_upload(image):
    buffer = BytesIO()
    # Сохранение изображения в буфере
    image.save(buffer, format='JPEG')
    image_to_upload = InMemoryUploadedFile(
        buffer,
        'avatar',
        'image/jpeg',
        buffer.tell(),
        None,
        None
    )
    return image_to_upload


def convert_to_image(inmemory_uploaded_file):
    # Создание буфера в памяти
    buffer = BytesIO()

    # Запись данных из InMemoryUploadedFile в буфер
    for chunk in inmemory_uploaded_file.chunks():
        buffer.write(chunk)
    buffer.seek(0)

    # Создание объекта Image из буфера
    image = Image.open(buffer)

    return image


class CropFace(object):

    def __init__(self, width=None, height=None, upscale=None, margin_percent: float = 0.5):
        self.width = width
        self.height = height
        self.upscale = upscale
        self.margin_percent = margin_percent

    def get_frame(self, image_size: tuple, face_borders: Borders = None) -> Borders:
        image_width, image_height = image_size
        if face_borders is None:
            return get_square_borders(image_width=image_width, image_height=image_height)

        face_high = face_borders.bottom - face_borders.top
        face_width = face_borders.right - face_borders.left
        face_size = face_width if face_width >= face_high else face_high
        margin = face_size * self.margin_percent

        left = face_borders.left - margin if face_borders.left - margin >= 0 else 0
        right = face_borders.right + margin if face_borders.right + margin <= image_width else image_width
        top = face_borders.top - margin if face_borders.top - margin >= 0 else 0
        bottom = face_borders.bottom + margin if face_borders.bottom + margin <= image_height else image_height

        margin = min(face_borders.left - left,
                     right - face_borders.right,
                     face_borders.top - top,
                     bottom - face_borders.bottom)

        left = face_borders.left - margin
        right = face_borders.right + margin
        top = face_borders.top - margin
        bottom = face_borders.bottom + margin

        return Borders(left=left, top=top, right=right, bottom=bottom)

    def crop_face(self, uploaded_image):
        try:
            face = find_face(uploaded_image)
        except NoFacesError:
            face_borders = None
            print('Лиц нет')
        except MultiplyFacesError:
            face_borders = None
            print('Много лиц')
        else:
            face_borders = get_face_borders(face)
            print('==================')
            print(face_borders)
        if isinstance(uploaded_image, InMemoryUploadedFile):
            image_file = convert_to_image(uploaded_image)
        elif isinstance(uploaded_image, Image.Image):
            image_file = uploaded_image
        else:
            raise TypeError('ожидается файл изображения')
        size = image_file.size
        avatar_borders = self.get_frame(image_size=size, face_borders=face_borders)
        cropped_image = image_file.crop(avatar_borders)
        return cropped_image


class CropFaceProcessor(CropFace):

    def process(self, img):
        return self.crop_face(img)


if __name__ == '__main__':
    img = Image.open('IMG_20230702_192926.jpg')
    # find_face(img)
