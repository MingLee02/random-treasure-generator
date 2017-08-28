from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.urls import reverse

from .models import Trinket


class TrinketListView(ListView):
    template_name = 'frostgrave/trinket/trinket-list.html'
    model = Trinket
    query_set = model.objects.all()
    paginate_by = 10


class TrinketView(DetailView):
    template_name = 'frostgrave/trinket/trinket.html'
    model = Trinket


class UpdateTrinketView(UpdateView):
    template_name = 'frostgrave/crud/update.html'
    model = Trinket
    fields = '__all__'

    def get_success_url(self):
        return reverse('frostgrave_trinket', kwargs={'pk': self.object.pk})


class DeleteTrinketView(DeleteView):
    template_name = 'frostgrave/crud/delete.html'
    model = Trinket

    def get_success_url(self):
        return reverse('frostgrave_trinkets')


class CreateTrinketView(CreateView):
    template_name = 'frostgrave/crud/create.html'
    model = Trinket
    fields = '__all__'

    def get_success_url(self):
        return reverse('frostgrave_trinket', kwargs={'pk': self.object.pk})
