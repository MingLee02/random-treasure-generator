from random import randint, choice
import xlrd
from xlrd import open_workbook, cellname
import pandas as pd

from django.apps import apps
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render
from django.http import QueryDict
from django.urls import reverse
from django.utils.datastructures import MultiValueDict

from .models import Equipment, Grimoire, Scroll, Trinket
from .constants import RARITY, TREASURE_TYPES
from .utils import *


def create_objects(sheet, values):
    if sheet == 'trinkets':
        create_trinkets(values)
    elif sheet == 'scrolls':
        create_scrolls(values)
    elif sheet == 'grimoires':
        create_grimoires(values)
    elif sheet == 'equipment':
        create_equipment(values)

def post(request):
    if request.method == "POST":
        workbook = pd.ExcelFile(request._files['file'])
        sheets = (workbook.sheet_names)

        for sheet in sheets:
            book = pd.read_excel(workbook, sheet_name=sheet)
            values = book.to_dict('records')

            create_objects(sheet.lower(), values)

    messages.success(request, 'Spreadsheet Processed')
    return render(request, 'frostgrave/main.html')

def random(request):
    try:
        non_specific = request._post['num']
    except KeyError:
        non_specific = None

    if non_specific is None:
        try:
            specfic =  request._post['type']
            value = request._post['value']
        except KeyError:
            return

    treasure = []
    rarity = RARITY
    treasure_type = TREASURE_TYPES

    if non_specific:
        for num in range(0, int(non_specific)):
            random = choice(treasure_type)
            if random == 'es':
                breaker = randint(1, 2)
                if breaker == 1:
                    random = 'Equipment'
                else:
                    random = 'Scroll'
            model = apps.get_model(app_label='frostgrave', model_name=random)

            if random == 'Trinket':
                treasure.append({
                    'data': model.objects.order_by('?')[:1].first(),
                    'page': 'trinket',
                })
            else:
                rare = choice(rarity)
                rare = rare.upper()
                treasure.append({
                    'data': model.objects.filter(rarity=rare).order_by('?')[:1].first(),
                    'page': random,
                })
    else:
        model = apps.get_model(app_label='frostgrave', model_name=specfic)
        num = int(value)

        if specfic == 'Trinket':
            items = model.objects.order_by('?')[:num]

            for item in items:
                treasure.append({
                    'data': item,
                    'page': 'trinket',
                })
        else:
            rare = choice(rarity)
            rare = rare.upper()
            items = model.objects.filter(rarity=rare).order_by('?')[:num]
            for item in items:
                treasure.append({
                    'data': item,
                    'page': specfic,
                })

    return render(request, 'frostgrave/main.html', {
        'treasures': treasure
    })


class UploadSheetView(TemplateView):
    template_name = 'frostgrave/upload.html'


class MainView(TemplateView):
    template_name = 'frostgrave/main.html'

item_dict = [
    {
        'name': 'trinket',
        'model': Trinket,
        'list-template': 'frostgrave/trinket/list.html',
        'template': 'frostgrave/trinket/detail.html'
    },
    {
        'name': 'scroll',
        'model': Scroll,
        'list-template': 'frostgrave/scroll/list.html',
        'template': 'frostgrave/scroll/detail.html'
    },
    {
        'name': 'grimoire',
        'model': Grimoire,
        'list-template': 'frostgrave/grimoire/list.html',
        'template': 'frostgrave/grimoire/detail.html'
    },
    {
        'name': 'equipment',
        'model': Equipment,
        'list-template': 'frostgrave/equipment/list.html',
        'template': 'frostgrave/equipment/detail.html'
    },
]

class ItemListView(ListView):
    paginate_by = 10

    def get_item(self):
        return [x for x in item_dict if x['name'] == self.kwargs['item']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_template_names(self):
        return self.get_item()[0]['list-template']


class ItemView(DetailView):
    def get_item(self):
        return [x for x in item_dict if x['name'] == self.kwargs['item_detail']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_template_names(self):
        return self.get_item()[0]['template']


class UpdateItemView(UpdateView):
    template_name = 'frostgrave/crud/update.html'
    fields = '__all__'

    def get_item(self):
        return [x for x in item_dict if x['name'] == self.kwargs['item_edit']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_context_data(self, **kwargs):
        context = super(UpdateItemView, self).get_context_data(**kwargs)
        context['items'] = self.get_item()[0]['name']
        return context

    def get_success_url(self):
        return reverse('item', kwargs={
            'item_detail': self.get_item()[0]['name'],
            'pk': self.object.pk
        })


class DeleteItemView(DeleteView):
    template_name = 'frostgrave/crud/delete.html'

    def get_item(self):
        return [x for x in item_dict if x['name'] == self.kwargs['item_delete']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_context_data(self, **kwargs):
        context = super(DeleteItemView, self).get_context_data(**kwargs)
        context['items'] = self.get_item()[0]['name']
        return context

    def get_success_url(self):
        return reverse('items', kwargs={'item': self.get_item()[0]['name']})


class CreateItemView(CreateView):
    template_name = 'frostgrave/crud/create.html'
    fields = '__all__'

    def get_item(self):
        return [x for x in item_dict if x['name'] == self.kwargs['item_create']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_context_data(self, **kwargs):
        context = super(CreateItemView, self).get_context_data(**kwargs)
        context['items'] = self.get_item()[0]['name']
        return context

    def get_success_url(self):
        return reverse('item', kwargs={
            'item_detail': self.get_item()[0]['name'],
            'pk': self.object.pk
        })
