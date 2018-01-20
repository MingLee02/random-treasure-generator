from random import randint, choice
import xlrd
from xlrd import open_workbook, cellname

from django.apps import apps
from django.contrib import messages
from django.db import transaction
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render
from django.http import QueryDict
from django.urls import reverse
from django.utils.datastructures import MultiValueDict

from .models import Equipment, Grimoire, Scroll, Trinket

@transaction.atomic
def create_equipment(values):
    for value in values:
        if len(value[0]) > 0:
            Equipment.objects.update_or_create(
                rarity=value[0],
                equip_type=value[1],
                name=value[2],
                description=value[3],
                effect=value[4],
                use=value[5],
                cost=value[6],
            )

@transaction.atomic
def create_grimoires(values):
    for value in values:
        if len(value[0]) > 0:
            Grimoire.objects.update_or_create(
                rarity=value[0],
                school=value[1],
                name=value[2],
                cost=value[3],
                target=value[4],
                grimoire_range=value[5],
                effect=value[6],
                duration=value[7],
                defence=value[8],
                value=value[9]
            )

@transaction.atomic
def create_scrolls(values):
    for value in values:
        if len(value[0]) > 0:
            Scroll.objects.update_or_create(
                rarity=value[0],
                school=value[1],
                name=value[2],
                cost=value[3],
                target=value[4],
                scroll_range=value[5],
                effect=value[6],
                duration=value[7],
                defence=value[8],
                value=value[9]
            )

@transaction.atomic
def create_trinkets(values):
    for value in values:
        if len(value[0]) > 0:
            Trinket.objects.update_or_create(
                rarity=value[0],
                description=value[1],
                name=value[2],
                effect=value[3],
                use=value[4],
                school=value[5],
                cost=value[6]
            )

def open_workbook(workbook):
    mdict = MultiValueDict(workbook)
    qdict = QueryDict('', mutable=True)
    qdict.update(mdict)
    return qdict

def create_model_objects_from_spreadsheet(wb):
    for name in wb.sheet_names():
        sheet = wb.sheet_by_name(name)
        values = [sheet.row_values(i) for i in range(1, sheet.nrows)]
        
        if name == 'Trinkets':
            create_trinkets(values)
        elif name == 'Scrolls':
            create_scrolls(values)
        elif name == 'Grimoires':
            create_grimoires(values)
        elif name == 'Equipment':
            create_equipment(values)

def post(request):
    if request.method == "POST":

        workbook = open_workbook(request._files)
        item_count = 0

        if "xls" in workbook['file']._name:
            wb = xlrd.open_workbook(filename=None, file_contents=qdict['file'].read())
            create_model_objects_from_spreadsheet(wb)

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
    rarity = [
        'common', 'common', 'common', 'common', 'common',
        'uncommon', 'uncommon', 'uncommon',
        'rare', 'rare'
    ]

    treasure_type = [
        'Trinket', 'Trinket', 'Trinket', 'Trinket', 'Trinket',
        'Equipment', 'Scroll', 'Scroll',
        'es', 'Grimoire'
    ]

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