# mysite/admin.py

from django.contrib import admin
from ..models import Equipment

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('unit_name', 'location', 'area_served', 'filter_size', 'filters_due', 'belts', 'notes', 'filter_rotation', 'filter_type', 'filters_last_changed', 'assigned_to', 'image')
