from django.db import models


class Trinket(models.Model):
    visual_description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    effect_description = models.TextField(null=True, blank=True)
    uses = models.CharField(max_length=255, null=True, blank=True)
    school_magic = models.CharField(max_length=255, null=True, blank=True)
    cost =  models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Potion(models.Model):
    visual_description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    effect_description = models.TextField(null=True, blank=True)
    uses = models.CharField(max_length=255, null=True, blank=True)
    cost =  models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class AdventurersGear(models.Model):
    visual_description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    effect_description = models.TextField(null=True, blank=True)
    uses = models.CharField(max_length=255, null=True, blank=True)
    cost =  models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Spell(models.Model):
    school = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    cost = models.CharField(max_length=255, null=True, blank=True)
    target = models.CharField(max_length=255, null=True, blank=True)
    book_ammends = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class EquipmentType(models.Model):
    item_type = models.CharField(max_length=255)
    
    def __str__(self):
        return self.item_type


class Equipment(models.Model):
    weight = models.CharField(max_length=255)
    item_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        related_name="type",
    )
    item = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['item']

    def __str__(self):
        return self.item

