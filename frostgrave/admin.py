from django.contrib import admin
from .models import AdventurersGear, Equipment, EquipmentType, Potion, Spell, Trinket


admin.site.register(AdventurersGear)
admin.site.register(Equipment)
admin.site.register(EquipmentType)
admin.site.register(Potion)
admin.site.register(Spell)
admin.site.register(Trinket)