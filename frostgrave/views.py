from random import randint, choice
import pandas as pd

from django.apps import apps
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render
from django.http import QueryDict
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q

from .constants import RARITY, TREASURE_TYPES, ITEMS
from .utils import *
from .models import Equipment, Grimoire, Scroll, Trinket


def build_result_set(results, type):
    results_list = []

    for result in results:
        item_dict = {
            'id': result.id,
            'name': result.name
        }

        try:
            item_dict['description'] = result.description
        except AttributeError:
            pass

        try:
            item_dict['effect'] = result.effect
        except AttributeError:
            pass

        try:
            item_dict['school'] = result.school
        except AttributeError:
            pass

        item_dict['model'] = type

        results_list.append(item_dict)
    return results_list

def search(request):
    search_term = request.GET['q']

    equipment = Equipment.objects.filter(
        Q(cost__contains=search_term) | Q(description__contains=search_term) | Q(effect__contains=search_term)
        | Q(equip_type__contains=search_term) | Q(name__contains=search_term) | Q(rarity__contains=search_term)
        | Q(use__contains=search_term)
    )
    equipment_list = build_result_set(equipment, 'equipment')

    trinket = Trinket.objects.filter(
        Q(cost__contains=search_term) | Q(description__contains=search_term) | Q(effect__contains=search_term)
        | Q(name__contains=search_term) | Q(rarity__contains=search_term) | Q(school__contains=search_term)
        | Q(use__contains=search_term)
    )
    trinket_list = build_result_set(trinket, 'trinket')

    scroll = Scroll.objects.filter(
        Q(cost__contains=search_term) | Q(defence__contains=search_term) | Q(duration__contains=search_term)
        | Q(effect__contains=search_term) | Q(name__contains=search_term) | Q(rarity__contains=search_term)
        | Q(school__contains=search_term) | Q(scroll_range__contains=search_term) | Q(target__contains=search_term)
        | Q(value__contains=search_term)
    )
    scroll_list = build_result_set(scroll, 'scroll')

    grimoire = Grimoire.objects.filter(
        Q(cost__contains=search_term) | Q(defence__contains=search_term) | Q(duration__contains=search_term)
        | Q(effect__contains=search_term) | Q(grimoire_range__contains=search_term) | Q(name__contains=search_term)
        | Q(rarity__contains=search_term) | Q(school__contains=search_term) | Q(target__contains=search_term)
        | Q(value__contains=search_term)
    )
    grimoire_list = build_result_set(grimoire, 'grimoire')

    results_list = trinket_list + equipment_list + scroll_list + grimoire_list

    return render(request, 'frostgrave/search-results.html', {
        'treasures': results_list
    })

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

        sheets = workbook.sheet_names

        for sheet in sheets:
            book = pd.read_excel(workbook, sheet_name=sheet)
            book = book.dropna()
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
            'page': specific,
        })

    return response

def random(request):
    specific = None
    try:
        specific = request._post['type']
        value = request._post['value']
    except KeyError:
        return

    treasure_type = TREASURE_TYPES

    if specific == 'Random':
        treasure = get_treasure(value, treasure_type)
    else:
        treasure = get_specific_treasure(specific, value)

    print(specific)
    return render(request, 'frostgrave/main.html', {
        'treasures': treasure,
        "option": specific.replace(" ", "")
    })

class UploadSheetView(TemplateView):
    template_name = 'frostgrave/upload.html'

class MainView(TemplateView):
    template_name = 'frostgrave/main.html'

class ItemListView(ListView):
    paginate_by = 20

    def get_item(self):
        return [x for x in ITEMS if x['name'] == self.kwargs['item']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all().order_by('name')

    def get_template_names(self):
        return self.get_item()[0]['list-template']


class ItemView(DetailView):
    def get_item(self):
        return [x for x in ITEMS if x['name'] == self.kwargs['item_detail']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_template_names(self):
        return self.get_item()[0]['template']


def set_context(view, self, **kwargs):
    context = super(view, self).get_context_data(**kwargs)
    context['items'] = self.get_item()[0]['name']
    return context


class UpdateItemView(UpdateView):
    template_name = 'frostgrave/crud/update.html'
    fields = '__all__'

    def get_item(self):
        return [x for x in ITEMS if x['name'] == self.kwargs['item_edit']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_context_data(self, **kwargs):
        return set_context(UpdateItemView, self, **kwargs)

    def get_success_url(self):
        return reverse('item', kwargs={
            'item_detail': self.get_item()[0]['name'],
            'pk': self.object.pk
        })


class DeleteItemView(DeleteView):
    template_name = 'frostgrave/crud/delete.html'

    def get_item(self):
        return [x for x in ITEMS if x['name'] == self.kwargs['item_delete']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_context_data(self, **kwargs):
        return set_context(DeleteItemView, self, **kwargs)

    def get_success_url(self):
        return reverse('items', kwargs={'item': self.get_item()[0]['name']})


class CreateItemView(CreateView):
    template_name = 'frostgrave/crud/create.html'
    fields = '__all__'

    def get_item(self):
        return [x for x in ITEMS if x['name'] == self.kwargs['item_create']]

    def get_queryset(self):
        return self.get_item()[0]['model'].objects.all()

    def get_context_data(self, **kwargs):
        return set_context(CreateItemView, self, **kwargs)

    def get_success_url(self):
        return reverse('item', kwargs={
            'item_detail': self.get_item()[0]['name'],
            'pk': self.object.pk
        })
