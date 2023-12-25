from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView


from listings.forms import CreateOfferForm
from listings.models import Listing

User = get_user_model()


class OfferCreateView(CreateView):
    model = Listing
    form_class = CreateOfferForm
    template_name = 'listings/listing_form.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Создание программы'}

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.specialist = self.request.user
        listing.duration = form.cleaned_data['duration']
        listing.save()
        return super().form_valid(form)


class OfferUpdateView(OfferCreateView, UpdateView):

    def get_initial(self):
        initial = super().get_initial()
        listing = self.get_object()
        duration = listing.duration
        initial['hours'] = duration.days * 24 + duration.seconds // 3600
        initial['minutes'] = (duration.seconds // 60) % 60
        return initial


def remove_offer(request, pk):
    offer = Listing.objects.get(pk=pk)
    offer.delete()
    return redirect('users:profile')
