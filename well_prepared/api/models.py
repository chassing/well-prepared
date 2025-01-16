import datetime

from django.db import models


#
# Templates
#
class EventTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering: tuple[str] = ("-name",)

    def __str__(self) -> str:
        return self.name


class SectionTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    event = models.ForeignKey(
        EventTemplate, on_delete=models.CASCADE, related_name="sections"
    )

    class Meta:
        ordering: tuple[str] = ("name",)

    def __str__(self) -> str:
        return f"{self.event}/{self.name}"


class ItemTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    section = models.ForeignKey(
        SectionTemplate, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        ordering: tuple[str] = ("name",)

    def __str__(self) -> str:
        return f"{self.section}/{self.name}"


#
# Real Instances
#
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    date = models.DateField()
    open = models.BooleanField(default=True)

    class Meta:
        ordering: tuple[str] = ("date", "name")

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create_from_template(
        cls, name: str, date: datetime.date, template: EventTemplate
    ) -> "Event":
        event = Event.objects.create(
            name=name, date=date, description=template.description, icon=template.icon
        )
        for section_template in template.sections.all():
            section = Section.objects.create(
                name=section_template.name,
                description=section_template.description,
                icon=section_template.icon,
                event=event,
            )
            for item_template in section_template.items.all():
                Item.objects.create(
                    name=item_template.name,
                    description=item_template.description,
                    icon=item_template.icon,
                    section=section,
                )
        return event

    def toggle_open(self) -> None:
        self.open = not self.open
        self.save()


class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sections")
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
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="items")

    class Meta:
        ordering: tuple[str] = ("name",)

    def __str__(self) -> str:
        return self.name

    def toggle_status(self) -> None:
        self.status = "O" if self.status == "C" else "C"
        self.save()
