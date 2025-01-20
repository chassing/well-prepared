from typing import Any

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from api.models import (
    Category,
    Event,
    Item,
    Template,
    TemplateCategory,
    TemplateItem,
)
from frontend.forms import (
    EventForm,
    FileUploadForm,
    TemplateCategoryForm,
    TemplateForm,
    TemplateItemCreateForm,
    TemplateItemEditForm,
)
from utils.emoji import matching_emojis, random_emoji


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]

    status_code = 200


@login_required
def empty(_: HttpRequest) -> HttpResponse:
    return HttpResponse("")


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "dashboard.html",
        {
            "events": Event.objects.prefetch_related(
                "categories", "categories__items"
            ).filter(open=True)
        },
    )


@login_required
def template_list(request: HttpRequest) -> HttpResponse:
    return render(request, "template-list.html", {"templates": Template.objects.all()})


@login_required
def template_detail(request: HttpRequest, template_pk: int) -> HttpResponse:
    return render(
        request,
        "template-detail.html",
        {
            "template": get_object_or_404(
                Template.objects.prefetch_related("categories", "categories__items"),
                pk=template_pk,
            )
        },
    )


@login_required
def template_create(request: HttpRequest) -> HttpResponse:
    form = TemplateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.instance.author = request.user
        obj = form.save()
        return HttpResponseRedirect(
            reverse("frontend:template-detail", kwargs={"template_pk": obj.pk})
        )
    return render(request, "template-create.html", {"form": form})


@login_required
def template_edit(request: HttpRequest, template_pk: int) -> HttpResponse:
    template = get_object_or_404(Template, pk=template_pk)
    form = TemplateForm(request.POST or None, instance=template)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect(
            reverse("frontend:template-detail", kwargs={"template_pk": template.pk})
        )
    return render(
        request, "template-edit.html", {"form": form, "template_pk": template.pk}
    )


@login_required
def template_export(_: HttpRequest, template_pk: int) -> HttpResponse:
    template = get_object_or_404(
        Template.objects.prefetch_related("categories", "categories__items"),
        pk=template_pk,
    )
    return HttpResponse(
        template.export_data(),
        content_type="application/yaml",
        headers={"content-disposition": f"attachment; filename={template.name}.yaml"},
    )


@login_required
def template_import(request: HttpRequest) -> HttpResponse:
    form = FileUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        template = Template.import_data(
            author=request.user, data=form.cleaned_data["file"]
        )
        return HttpResponseRedirect(
            reverse("frontend:template-detail", kwargs={"template_pk": template.pk})
        )
    return render(request, "template-import.html", {"form": form})


@login_required
def template_delete(request: HttpRequest, template_pk: int) -> HttpResponse:
    template = get_object_or_404(Template, pk=template_pk)
    if request.method == "POST":
        template.delete()
        return HTTPResponseHXRedirect(redirect_to=reverse("frontend:template-list"))
    return HttpResponseNotAllowed(["POST"])


@login_required
def template_category_create(request: HttpRequest, template_pk: int) -> HttpResponse:
    template = get_object_or_404(Template, pk=template_pk)
    form = TemplateCategoryForm(request.POST or None)
    form.instance.template = template
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect(
            reverse("frontend:template-detail", kwargs={"template_pk": template.pk})
        )
    return render(
        request,
        "template-category-create.html",
        {"form": form, "template_pk": template.pk},
    )


@login_required
def template_item_create(request: HttpRequest, category_pk: int) -> HttpResponse:
    category = get_object_or_404(TemplateCategory, pk=category_pk)
    form = TemplateItemCreateForm(request.POST or None)
    form.instance.category = category
    if request.method == "POST" and form.is_valid():
        form.instance.icon = random_emoji(form.instance.name)
        form.save()
        return HttpResponseRedirect(
            reverse(
                "frontend:template-item-detail", kwargs={"item_pk": form.instance.pk}
            )
        )
    return render(
        request,
        "partials/template-item-create.html",
        {"form": form, "category_pk": category.pk},
    )


@login_required
def template_item_edit(request: HttpRequest, item_pk: int) -> HttpResponse:
    obj = get_object_or_404(TemplateItem, pk=item_pk)
    form = TemplateItemEditForm(request.POST or None, instance=obj)
    emojis = {*matching_emojis(obj.name), obj.icon, ""}
    form.fields["icon"].widget.choices = [(e, e) for e in sorted(emojis)]
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect(
            reverse(
                "frontend:template-item-detail", kwargs={"item_pk": form.instance.pk}
            )
        )
    return render(request, "partials/template-item-edit.html", {"form": form})


@login_required
def template_item_detail(request: HttpRequest, item_pk: int) -> HttpResponse:
    return render(
        request,
        "partials/template-item-detail.html",
        {"item": get_object_or_404(TemplateItem, pk=item_pk)},
    )


@login_required
def template_item_delete(request: HttpRequest, item_pk: int) -> HttpResponse:
    item = get_object_or_404(TemplateItem, pk=item_pk)
    if request.method == "POST":
        item.delete()
        return HttpResponse("")
    return HttpResponseNotAllowed(["POST"])


#
# Events
#


@login_required
def event_create(request: HttpRequest, template_pk: int) -> HttpResponse:
    event_tmpl = get_object_or_404(Template, pk=template_pk)
    form = EventForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.instance.author = request.user
        obj = form.save(event_tmpl)
        return HttpResponseRedirect(
            reverse("frontend:event-detail", kwargs={"event_pk": obj.pk})
        )

    return render(request, "event-create.html", {"form": form, "template": event_tmpl})


@login_required
def event_list(request: HttpRequest) -> HttpResponse:
    return render(request, "event-list.html", {"events": Event.objects.all()})


@login_required
def event_detail(request: HttpRequest, event_pk: int) -> HttpResponse:
    return render(
        request, "event-detail.html", {"event": get_object_or_404(Event, pk=event_pk)}
    )


@login_required
def event_toggle_open(request: HttpRequest, event_pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=event_pk)
    if request.method == "POST":
        event.toggle_open()

    return HTTPResponseHXRedirect(
        reverse("frontend:event-detail", kwargs={"event_pk": event.pk})
    )


@login_required
def category_toggle_display_closed_items(
    request: HttpRequest, category_pk: int
) -> HttpResponse:
    category = get_object_or_404(Category, pk=category_pk)
    if request.method == "POST":
        category.toggle_display_closed_items()

    return render(request, "partials/item-list.html", {"category": category})


@login_required
def item_toggle_status(request: HttpRequest, item_pk: int) -> HttpResponse:
    item = get_object_or_404(Item, pk=item_pk)
    if request.method == "POST":
        item.toggle_status()

    return render(
        request,
        "partials/item-detail.html",
        {"item": item, "display_closed_items": item.category.display_closed_items},
    )


@login_required
def item_list(request: HttpRequest, category_pk: int) -> HttpResponse:
    category = get_object_or_404(
        Category.objects.prefetch_related("items"), pk=category_pk
    )
    return render(request, "partials/item-list.html", {"category": category})
