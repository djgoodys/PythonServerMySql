# mysite/models.py

from django.db import models

class Equipment(models.Model):
    _id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=40)
    location = models.CharField(max_length=40)
    area_served = models.CharField(max_length=40)
    filter_size = models.CharField(max_length=60)
    filters_due = models.DateField()
    belts = models.CharField(max_length=30)
    notes = models.CharField(max_length=200)
    filter_rotation = models.IntegerField()
    filter_type = models.CharField(max_length=20)
    filters_last_changed = models.CharField(max_length=15, null=True, blank=True)
    assigned_to = models.CharField(max_length=10)
    image = models.CharField(max_length=20)

    def __str__(self):
        return self.unit_name
