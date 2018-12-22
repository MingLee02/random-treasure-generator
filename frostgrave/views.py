from random import randint, choice
import pandas as pd

from django.apps import apps
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render
from django.http import QueryDict
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from .constants import RARITY, TREASURE_TYPES, ITEMS
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
        try:
            workbook = pd.ExcelFile(request._files['file'])
        except MultiValueDictKeyError:
            messages.error(request, 'You have to actually add a excel file')
            return render(request, 'frostgrave/upload.html')

        sheets = (workbook.sheet_names)

        for sheet in sheets:
            book = pd.read_excel(workbook, sheet_name=sheet)
            values = book.to_dict('records')

            create_objects(sheet.lower(), values)

    messages.success(request, 'Spreadsheet Processed')
    return render(request, 'frostgrave/main.html')

def get_treasure(quantity, treasure_type):
    response = []
    for num in range(0, int(quantity)):
        random = choice(treasure_type)
        if random == 'es':
            breaker = randint(1, 2)
            if breaker == 1:
                random = 'Equipment'
            else:
                random = 'Scroll'
        model = apps.get_model(app_label='frostgrave', model_name=random)

        if random == 'Trinket':
            items =  model.objects.order_by('?')[:1].first()
        else:
            rare = choice(RARITY).upper()
            items = model.objects.filter(rarity=rare).order_by('?')[:1].first()

        response.append({
            'data': items,
            'page': random,
        })
    return response

def get_specific_treasure(specific, value):
    response = []
    model = apps.get_model(app_label='frostgrave', model_name=specific)
    num = int(value)

    if specific == 'Trinket':
        items = model.objects.order_by('?')[:num]
    else:
        rare = choice(RARITY).upper()
        items = model.objects.filter(rarity=rare).order_by('?')[:num]

    for item in items:
        response.append({
            'data': item,
            'page': 'trinket',
        })

    return response


def random(request):
    try:
        non_specific = request._post['num']
    except KeyError:
        non_specific = None

    if non_specific is None:
        try:
            specific = request._post['type']
            value = request._post['value']
        except KeyError:
            return

    treasure_type = TREASURE_TYPES

    if non_specific:
        treasure = get_treasure(non_specific, treasure_type)
    else:
        treasure = get_specific_treasure(specific, value)

    return render(request, 'frostgrave/main.html', {
        'treasures': treasure
    })


class UploadSheetView(TemplateView):
    template_name = 'frostgrave/upload.html'


class MainView(TemplateView):
    template_name = 'frostgrave/main.html'


class ItemListView(ListView):
    paginate_by = 10

    def get_item(self):
        return [x for x in ITEMS if x['name'] == self.kwargs['item']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_template_names(self):
        return self.get_item()[0]['list-template']


class ItemView(DetailView):
    def get_item(self):
        return [x for x in ITEMS if x['name'] == self.kwargs['item_detail']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_template_names(self):
        return self.get_item()[0]['template']


class UpdateItemView(UpdateView):
    template_name = 'frostgrave/crud/update.html'
    fields = '__all__'

    def get_item(self):
        return [x for x in ITEMS if x['name'] == self.kwargs['item_edit']]

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
