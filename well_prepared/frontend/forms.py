from django import forms

from api.models import Event, Template, TemplateCategory, TemplateItem


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ("name", "description", "icon")

    def clean_name(self) -> str:
        name: str = self.cleaned_data["name"]
        if Template.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                f"A template with the name {name} already exists"
            )
        return name


class FileUploadForm(forms.Form):
    file = forms.FileField(label="Select a file")


class TemplateCategoryForm(forms.ModelForm):
    class Meta:
        model = TemplateCategory
        fields = ("name", "description", "icon")

    def clean_name(self) -> str:
        name: str = self.cleaned_data["name"]
        if (
            TemplateCategory.objects.filter(name=name, template=self.instance.template)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                f"A category with the name {name} already exists"
            )
        return name


class TemplateItemCreateForm(forms.ModelForm):
    class Meta:
        model = TemplateItem
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"data-1p-ignore": "true"}),
        }

    def clean_name(self) -> str:
        name: str = self.cleaned_data["name"]
        if (
            TemplateItem.objects.filter(
                name=name, category__template=self.instance.category.template
            )
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(f"An item with the name {name} already exists")
        return name


class TemplateItemEditForm(forms.ModelForm):
    class Meta:
        model = TemplateItem
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"data-1p-ignore": "true"}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "date")
        widgets = {
            "name": forms.TextInput(attrs={"data-1p-ignore": "true"}),
        }

    def clean_name(self) -> str:
        name: str = self.cleaned_data["name"]
        if (
            Event.objects.filter(name=name, open=True)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(f"An event with the name {name} already exists")
        return name

    def save(self, template: Template) -> Event:
        return Event.create_from_template(
            name=self.cleaned_data["name"],
            date=self.cleaned_data["date"],
            template=template,
        )
