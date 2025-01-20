import datetime
from collections.abc import Mapping

import yaml
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


#
# Templates
#
class Template(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=10, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering: tuple = ("-name",)

    def __str__(self) -> str:
        return self.name

    def export_data(self) -> str:
        """Export the template to YAML."""
        data = {
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "categories": [],
        }
        for category in self.categories.all():
            category_data = {
                "name": category.name,
                "description": category.description,
                "icon": category.icon,
                "items": [],
            }
            for item in category.items.all():
                category_data["items"].append({
                    "name": item.name,
                    "description": item.description,
                })
            data["categories"].append(category_data)
        return yaml.dump(data, explicit_start=True, encoding="utf-8")

    @classmethod
    def import_data(cls, author: User, data: Mapping) -> "Template":
        """Import a template from YAML."""
        data = yaml.safe_load(data)
        template = cls.objects.create(
            name=f"{data['name']}-imported-{datetime.datetime.now(tz=datetime.UTC):%Y-%m-%d}",
            description=data["description"],
            icon=data["icon"],
            author=author,
        )
        for category_data in data["categories"]:
            category = TemplateCategory.objects.create(
                name=category_data["name"],
                description=category_data["description"],
                icon=category_data["icon"],
                template=template,
            )
            for item_data in category_data["items"]:
                TemplateItem.objects.create(
                    name=item_data["name"],
                    description=item_data["description"],
                    category=category,
                )
        return template


class TemplateCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        ordering: tuple = ("name",)

    def __str__(self) -> str:
        return f"{self.template}/{self.name}"


class TemplateItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        TemplateCategory, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        ordering: tuple = ("name",)

    def __str__(self) -> str:
        return f"{self.category}/{self.name}"


#
# Real Instances
#
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    date = models.DateField()
    open = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering: tuple = ("date", "name")

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create_from_template(
        cls, name: str, date: datetime.date, author: User, template: Template
    ) -> "Event":
        event = Event.objects.create(
            name=name,
            date=date,
            description=template.description,
            icon=template.icon,
            author=author,
        )
        for template_category in template.categories.all():
            category = Category.objects.create(
                name=template_category.name,
                description=template_category.description,
                icon=template_category.icon,
                event=event,
            )
            for template_item in template_category.items.all():
                Item.objects.create(
                    name=template_item.name,
                    description=template_item.description,
                    category=category,
                )
        return event

    def toggle_open(self) -> None:
        self.open = not self.open
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="categories"
    )
    display_closed_items = models.BooleanField(default=False)

    class Meta:
        ordering: tuple = ("name",)

    def __str__(self) -> str:
        return self.name

    def toggle_display_closed_items(self) -> None:
        self.display_closed_items = not self.display_closed_items
        self.save()

    @property
    def done(self) -> bool:
        return all(item.status == "C" for item in self.items.all())


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    MODES = {
        "O": "Open",
        "C": "Closed",
    }
    status = models.CharField(max_length=1, choices=MODES, default="O")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        ordering: tuple = ("name",)

    def __str__(self) -> str:
        return self.name

    def toggle_status(self) -> None:
        self.status = "O" if self.status == "C" else "C"
        self.save()
