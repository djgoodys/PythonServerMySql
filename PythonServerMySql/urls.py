from django.contrib import admin
from django.urls import path
from mysite import equipment_view
from mysite import users_view
from mysite import tasks_view
from mysite import filters_view
from mysite import filter_types_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/manageEquipment/', equipment_view.manageEquipment, name='manageEquipment'),
    path('api/manageFilters/', filters_view.manageFilters, name='manageFilters'),
    path('api/manageFilterTypes/', filter_types_view.manageFilterTypes, name='manageFilterTypes'),
    path('api/manageTasks/', tasks_view.manageTasks, name='manageTasks'),
    path('api/manageUsers/', users_view.manageUsers, name='manageUsers'),
    path('api/', equipment_view.welcome, name='welcome')
]

