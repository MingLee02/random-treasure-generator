from django.db import transaction
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