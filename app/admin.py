from django.contrib import admin
from .models import People, State, SchoolClass

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'school_class')

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('date', 'status')

admin.site.register(SchoolClass)
