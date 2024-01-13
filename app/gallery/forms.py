from pathlib import Path

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from multiupload.fields import MultiImageField
from django.core.validators import validate_image_file_extension


def validate_image_files_extension(value):
    for file in value:
        extension = Path(file.name).suffix[1:].lower()
        if extension not in ['jpg', 'jpeg', 'png', 'gif']:
            raise ValidationError('Допустимы только файлы с расширениями jpg, jpeg, png и gif.')


max_image_size_limit = settings.MAX_IMAGE_SIZE_LIMIT
max_image_size_text = f'Максимальный размер файла - {max_image_size_limit} Мб'


class AvatarForm(forms.Form):
    avatar = forms.ImageField(
        help_text=max_image_size_text,
        label='Аватар',
        required=False,
        widget=forms.ClearableFileInput()
    )


class MultiImageUploadForm(forms.Form):
    photos = MultiImageField(
        help_text=max_image_size_text,
        label='Добавить фотографии',
        min_num=1,
        max_num=10,
        max_file_size=1024 * 1024 * max_image_size_limit,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_photo_validators = self.fields['photos'].validators
        add_photo_validators.remove(validate_image_file_extension)
        add_photo_validators.append(validate_image_files_extension)
