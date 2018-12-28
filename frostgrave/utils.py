from django.db import transaction
from .models import Equipment, Grimoire, Scroll, Trinket

import pandas as pd

@transaction.atomic
def create_equipment(values):
    for value in values:
        value = {k.lower(): v for k, v in value.items()}
        value['equip_type'] = value['type']
        del value['type']
        if not pd.isnull(value['name']):
            Equipment.objects.update_or_create(**value)

@transaction.atomic
def create_grimoires(values):
    for value in values:
        value = {k.lower(): v for k, v in value.items()}
        value['value'] = value['cost.1']
        del value['cost.1']
        value['grimoire_range'] = value['range']
        del value['range']
        if not pd.isnull(value['name']):
            Grimoire.objects.update_or_create(**value)

@transaction.atomic
def create_scrolls(values):
    for value in values:
        value = {k.lower(): v for k, v in value.items()}
        value['scroll_range'] = value['range']
        del value['range']
        value['value'] = value['cost.1']
        del value['cost.1']
        Scroll.objects.update_or_create(**value)

@transaction.atomic
def create_trinkets(values):
    for value in values:
        value = {k.lower(): v for k, v in value.items()}
        Trinket.objects.update_or_create(**value)
