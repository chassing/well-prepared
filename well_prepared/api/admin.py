from django.contrib import admin

from .models import Event, EventTemplate, Item, ItemTemplate, Section, SectionTemplate


@admin.register(EventTemplate)
class EventTemplateAdmin(admin.ModelAdmin): ...


@admin.register(SectionTemplate)
class SectionTemplateAdmin(admin.ModelAdmin): ...


@admin.register(ItemTemplate)
class ItemTemplateAdmin(admin.ModelAdmin): ...


@admin.register(Event)
class EventAdmin(admin.ModelAdmin): ...


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin): ...


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin): ...
