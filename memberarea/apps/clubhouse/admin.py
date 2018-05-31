from django.contrib import admin

from .models import Clubhouse, Room, Defect
from .forms import DefectAdminForm


@admin.register(Clubhouse)
class ClubhouseAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'clubhouse')


@admin.register(Defect)
class DefectAdmin(admin.ModelAdmin):
    list_display = ('title', 'clubhouse', 'room', 'repaired')
    form = DefectAdminForm
