from django.db import models


class Trinket(models.Model):
    rarity = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    effect = models.TextField(null=True, blank=True)
    use = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    cost =  models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Scroll(models.Model):
    rarity = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    cost = models.CharField(max_length=255, null=True, blank=True)
    target = models.CharField(max_length=255, null=True, blank=True)
    scroll_range = models.CharField(max_length=255, null=True, blank=True)
    effect = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=255, null=True, blank=True)
    defence = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
 
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Grimoire(models.Model):
    rarity = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    cost = models.CharField(max_length=255, null=True, blank=True)
    target = models.CharField(max_length=255, null=True, blank=True)
    grimoire_range = models.CharField(max_length=255, null=True, blank=True)
    effect = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=255, null=True, blank=True)
    defence = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
 
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Equipment(models.Model):
    rarity = models.CharField(max_length=255, null=True, blank=True)
    equip_type = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    effect = models.TextField(null=True, blank=True)
    use = models.CharField(max_length=255, null=True, blank=True)
    cost = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
