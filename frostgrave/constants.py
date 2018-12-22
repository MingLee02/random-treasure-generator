from .models import Equipment, Grimoire, Scroll, Trinket

RARITY = [
    'common', 'common', 'common', 'common', 'common',
    'uncommon', 'uncommon', 'uncommon',
    'rare', 'rare'
]

TREASURE_TYPES = [
    'Trinket', 'Trinket', 'Trinket', 'Trinket', 'Trinket',
    'Equipment', 'Scroll', 'Scroll',
    'es', 'Grimoire'
]

ITEMS = [
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
