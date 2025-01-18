import datetime

from django.conf import settings
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
        ordering: tuple[str] = ("-name",)

    def __str__(self) -> str:
        return self.name


class TemplateCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        ordering: tuple[str] = ("name",)

    def __str__(self) -> str:
        return f"{self.template}/{self.name}"


class TemplateItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    category = models.ForeignKey(
        TemplateCategory, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        ordering: tuple[str] = ("name",)

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
        ordering: tuple[str] = ("date", "name")

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create_from_template(
        cls, name: str, date: datetime.date, template: Template
    ) -> "Event":
        event = Event.objects.create(
            name=name, date=date, description=template.description, icon=template.icon
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
                    icon=template_item.icon,
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
    display_closed_items = models.BooleanField(default=True)

    class Meta:
        ordering: tuple[str] = ("name",)

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
    icon = models.CharField(max_length=10, blank=True)
    MODES = {
        "O": "Open",
        "C": "Closed",
    }
    status = models.CharField(max_length=1, choices=MODES, default="O")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        ordering: tuple[str] = ("name",)

    def __str__(self) -> str:
        return self.name

    def toggle_status(self) -> None:
        self.status = "O" if self.status == "C" else "C"
        self.save()
