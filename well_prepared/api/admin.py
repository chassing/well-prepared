from django.contrib import admin

from .models import Category, Event, Item, Template, TemplateCategory, TemplateItem


@admin.register(Template)
class EventTemplateAdmin(admin.ModelAdmin): ...


@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin): ...


@admin.register(TemplateItem)
class TemplateItemAdmin(admin.ModelAdmin): ...


@admin.register(Event)
class EventAdmin(admin.ModelAdmin): ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): ...


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin): ...
