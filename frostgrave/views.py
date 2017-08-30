from random import randint, choice
import xlrd
from xlrd import open_workbook, cellname

from django.db import transaction
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render
from django.http import QueryDict
from django.urls import reverse

from django.utils.datastructures import MultiValueDict

from .models import AdventurersGear, Equipment, EquipmentType, Potion, Spell, Trinket

@transaction.atomic
def create_trinkets(values):
    for value in values:
        Trinket.objects.update_or_create(
            visual_description=value[0],
            name=value[1],
            effect_description=value[2],
            uses=value[3],
            school_magic=value[4],
            cost=value[5]
        )

@transaction.atomic
def create_potions(values):
    for value in values:
        Potion.objects.update_or_create(
            visual_description=value[0],
            name=value[1],
            effect_description=value[2],
            uses=value[3],
            cost=value[4]
        )

@transaction.atomic
def create_gear(values):
    for value in values:
        AdventurersGear.objects.update_or_create(
            visual_description=value[0],
            name=value[1],
            effect_description=value[2],
            uses=value[3],
            cost=value[4]
        )

@transaction.atomic
def create_spells(values):
    for value in values:
        Spell.objects.update_or_create(
            school=value[0],
            name=value[1],
            cost=value[2],
            target=value[3],
            book_ammends=value[4]
        )

@transaction.atomic
def create_equipment(weights, values):
    for value in values:
        counter = 0
        for item in value:
            if counter == 0:
                e_type = EquipmentType.objects.update_or_create(item_type=item)

            Equipment.objects.update_or_create(
                weight=weights[counter],
                item_type=e_type[0],
                item=item
            )
            counter = counter + 1

def get_equipment(equip):
    random = []
    items = Equipment.objects.filter(item_type=equip)
    for item in items:
        for num in  range(0, int(float(item.weight))):
            random.append(item)

    return choice(random)

def post(request):
    if request.method == "POST":
        mdict = MultiValueDict(request._files)
        qdict = QueryDict('', mutable=True)
        qdict.update(mdict)
        if "xls" in qdict['file']._name:
            wb = xlrd.open_workbook(filename=None, file_contents=qdict['file'].read())

            for name in wb.sheet_names():
                sheet = wb.sheet_by_name(name)

                if name == 'Weapons & Armour':
                    values = [sheet.col_values(i) for i in range(1, sheet.ncols)]
                    weight = sheet.col_values(0)
                    create_equipment(weight, values)
                else:
                    # read the rest rows for values
                    values = [sheet.row_values(i) for i in range(1, sheet.nrows)]

                    if name == 'Magical Trinkets':
                        create_trinkets(values)
                    elif name == 'Potions':
                        create_potions(values)
                    elif name == 'Adventurers Gear':
                        create_gear(values)
                    elif name == 'Spells':
                        create_spells(values)
          
    return render(request, 'frostgrave/main.html')


def random(request):
    random = randint(1, 5)

    if random == 1:
        table = 'Adventurers Gear'
        items = AdventurersGear.objects.order_by('?')[:int(request._post['num'])]
    elif random == 2:
        table = 'Potions'
        items = Potion.objects.order_by('?')[:int(request._post['num'])]
    elif random == 3:
        table = 'Spells'
        items = Spell.objects.order_by('?')[:int(request._post['num'])]
    elif random == 4:
        table = 'Trinkets'
        items = Trinket.objects.order_by('?')[:int(request._post['num'])]
    elif random == 5:
        table = 'Weapons & Armour'
        items = []
        for num in range(0, int(request._post['num'])):
            equip = EquipmentType.objects.order_by('?')[:1].first()
            items.append(get_equipment(equip))

    return render(request, 'frostgrave/main.html', {
        'items': items,
        'table': table
    })


class MainView(TemplateView):
    template_name = 'frostgrave/main.html'

item_dict = [
    {
        'name': 'trinkets',
        'model': Trinket,
        'list-template': 'frostgrave/trinket/list.html',
        'template': 'frostgrave/trinket/detail.html'
    },
    {   
        'name': 'potions',
        'model': Potion,
        'list-template': 'frostgrave/potion/list.html',
        'template': 'frostgrave/potion/detail.html'
    },
    {   
        'name': 'adventurers-gear',
        'model': AdventurersGear,
        'list-template': 'frostgrave/adventurersgear/list.html',
        'template': 'frostgrave/adventurersgear/detail.html'
    },
    {   
        'name': 'spells',
        'model': Spell,
        'list-template': 'frostgrave/spell/list.html',
        'template': 'frostgrave/spell/detail.html'
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