from django import forms

from api.models import Event, EventTemplate, ItemTemplate


class ItemTemplateForm(forms.ModelForm):
    class Meta:
        model = ItemTemplate
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"data-1p-ignore": "true"}),
        }

    def clean_name(self) -> str:
        name: str = self.cleaned_data["name"]
        if ItemTemplate.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"An item with the name {name} already exists")
        return name

    def save(self) -> ItemTemplate:
        item: ItemTemplate = super().save()
        return item


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "date")
        widgets = {
            "name": forms.TextInput(attrs={"data-1p-ignore": "true"}),
        }

    def clean_name(self) -> str:
        name: str = self.cleaned_data["name"]
        if Event.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"An event with the name {name} already exists")
        return name

    def save(self, template: EventTemplate) -> Event:
        return Event.create_from_template(
            name=self.cleaned_data["name"],
            date=self.cleaned_data["date"],
            template=template,
        )
