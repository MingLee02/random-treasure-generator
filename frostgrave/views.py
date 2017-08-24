from random import randint
import xlrd
from xlrd import open_workbook, cellname

from django.db import transaction
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

from .models import AdventurersGear, Potion, Spell, Trinket

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

def post(request):
    if request.method == "POST":
        mdict = MultiValueDict(request._files)
        qdict = QueryDict('', mutable=True)
        qdict.update(mdict)
        if "xls" in qdict['file']._name:
            wb = xlrd.open_workbook(filename=None, file_contents=qdict['file'].read())

            for name in wb.sheet_names():
                sheet = wb.sheet_by_name(name)
                keys = sheet.row_values(0)

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
    random = randint(1, 4)

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

    return render(request, 'frostgrave/main.html', {
        'items': items,
        'table': table
    })


class MainView(TemplateView):
    template_name = 'frostgrave/main.html'