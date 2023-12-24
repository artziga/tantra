
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView
from gallery.forms import AddPhotosForm
from gallery.models import Photo


def add_avatar(form, user, get='avatar'):
    image = form.files.get(get)
    if image:
        avatar = Photo.objects.create(image=image, user=user)
        avatar.make_as_avatar()


def add_photos(form, user, get='photos'):
    photos = form.files.getlist(get)
    if photos:
        for photo in photos:
            Photo.objects.create(image=photo, user=user)


class EditGallery(FormView):
    form_class = AddPhotosForm
    template_name = 'gallery/gallery_form.html'
    success_url = reverse_lazy('gallery:edit_gallery')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        specialist = self.request.user
        photos = Photo.objects.filter(user=specialist)
        context['title'] = 'Загрузка фото'
        context['photos'] = photos
        return context

    def form_valid(self, form):
        user = self.request.user
        add_avatar(form=form, user=user)
        add_photos(form=form, user=user)
        return super().form_valid(form)


class PhotoDeleteView(DeleteView):
    model = Photo

    def get_success_url(self):
        if self.request.user.is_specialist:
            return reverse_lazy('gallery:edit_gallery')
        return reverse_lazy('users:edit_profile', kwargs={'pk': self.request.user.pk})


def make_photo_as_avatar(photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    photo.make_as_avatar()


def change_avatar(request, pk):
    try:
        current_avatar = Photo.objects.get(user=request.user, is_avatar=True)
    except ObjectDoesNotExist:
        make_photo_as_avatar(photo_id=pk)
        return redirect('gallery:edit_gallery')
    new_avatar = get_object_or_404(Photo, id=pk)
    context = {'current_avatar': current_avatar, 'new_avatar': new_avatar}
    return render(request, template_name='gallery/change_avatar_confirmation.html', context=context)


def change_avatar_confirm(request, pk):
    make_photo_as_avatar(photo_id=pk)
    return redirect('gallery:edit_gallery')
