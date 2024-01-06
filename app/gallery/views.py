
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView
from gallery.forms import MultiImageUploadForm
from gallery.models import Photo
from gallery.utils import make_as_avatar, get_users_avatar


def add_avatar(form, user, get='avatar'):
    image = form.files.get(get)
    if image:
        photo = Photo.objects.create(image=image, user=user, is_avatar=True)
        make_as_avatar(photo)


def add_photos(form, user, get='photos'):
    photos = form.files.getlist(get)
    if photos:
        for photo in photos:
            Photo.objects.create(image=photo, user=user)


class EditGallery(FormView):
    form_class = MultiImageUploadForm
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


def change_avatar(request, pk):
    try:
        current_avatar = get_users_avatar(user=request.user)
    except ObjectDoesNotExist:
        photo = get_object_or_404(Photo, id=pk)
        make_as_avatar(photo=photo)
        return redirect('gallery:edit_gallery')
    new_avatar = get_object_or_404(Photo, id=pk)
    context = {'current_avatar': current_avatar, 'new_avatar': new_avatar}
    return render(request, template_name='gallery/change_avatar_confirmation.html', context=context)


def change_avatar_confirm(request, pk):
    photo = get_object_or_404(Photo, id=pk)
    make_as_avatar(photo=photo)
    return redirect('gallery:edit_gallery')
