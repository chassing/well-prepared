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
    Event,
    EventTemplate,
    Item,
    ItemTemplate,
    Section,
    SectionTemplate,
)
from frontend.forms import EventForm, ItemTemplateForm


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "dashboard.html",
        {
            "events": Event.objects.prefetch_related(
                "sections", "sections__items"
            ).filter(open=True)
        },
    )


@login_required
def template_list_view(request: HttpRequest) -> HttpResponse:
    return render(
        request, "template-list.html", {"templates": EventTemplate.objects.all()}
    )


@login_required
def template_detail_view(request: HttpRequest, template_pk: int) -> HttpResponse:
    return render(
        request,
        "template-detail.html",
        {
            "template": get_object_or_404(
                EventTemplate.objects.prefetch_related("sections", "sections__items"),
                pk=template_pk,
            )
        },
    )


@login_required
def item_template_create_view(request: HttpRequest, section_pk: int) -> HttpResponse:
    section = get_object_or_404(SectionTemplate, pk=section_pk)
    form = ItemTemplateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.instance.section = section
        form.save()
        return HttpResponseRedirect(
            reverse(
                "frontend:item-template-detail", kwargs={"item_pk": form.instance.pk}
            )
        )
    return render(
        request,
        "partials/item-template-create-form.html",
        {"form": form, "section_pk": section.pk},
    )


@login_required
def item_template_edit_view(request: HttpRequest, item_pk: int) -> HttpResponse:
    obj = get_object_or_404(ItemTemplate, pk=item_pk)
    form = ItemTemplateForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect(
            reverse(
                "frontend:item-template-detail", kwargs={"item_pk": form.instance.pk}
            )
        )
    return render(request, "partials/item-template-edit-form.html", {"form": form})


@login_required
def item_template_detail_view(request: HttpRequest, item_pk: int) -> HttpResponse:
    return render(
        request,
        "partials/item-template-detail.html",
        {"item": get_object_or_404(ItemTemplate, pk=item_pk)},
    )


@login_required
def item_template_delete_view(request: HttpRequest, item_pk: int) -> HttpResponse:
    item = get_object_or_404(ItemTemplate, pk=item_pk)
    if request.method == "POST":
        item.delete()
        return HttpResponse("")
    return HttpResponseNotAllowed(["POST"])


@login_required
def event_create_view(request: HttpRequest, template_pk: int) -> HttpResponse:
    event_tmpl = get_object_or_404(EventTemplate, pk=template_pk)
    form = EventForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(event_tmpl)
        return HttpResponseRedirect(
            reverse("frontend:event-detail", kwargs={"event_pk": obj.pk})
        )

    return render(request, "event-create.html", {"form": form, "template": event_tmpl})


@login_required
def event_detail_view(request: HttpRequest, event_pk: int) -> HttpResponse:
    return render(
        request, "event-detail.html", {"event": get_object_or_404(Event, pk=event_pk)}
    )


@login_required
def item_toggle_status_view(request: HttpRequest, item_pk: int) -> HttpResponse:
    item = get_object_or_404(Item, pk=item_pk)
    if request.method == "POST":
        item.toggle_status()

    return render(
        request,
        "partials/item-detail.html",
        {"item": item, "display_closed_items": item.section.display_closed_items},
    )


@login_required
def event_toggle_open_view(request: HttpRequest, event_pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=event_pk)
    if request.method == "POST":
        event.toggle_open()

    return render(request, "partials/event-toggle-open-button.html", {"event": event})


@login_required
def item_list_view(request: HttpRequest, section_pk: int) -> HttpResponse:
    section = get_object_or_404(
        Section.objects.prefetch_related("items"), pk=section_pk
    )
    return render(request, "partials/item-list.html", {"section": section})


@login_required
def section_toggle_display_closed_items_view(
    request: HttpRequest, section_pk: int
) -> HttpResponse:
    section = get_object_or_404(Section, pk=section_pk)
    if request.method == "POST":
        section.toggle_display_closed_items()

    return render(request, "partials/item-list.html", {"section": section})
