import django_tables2
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from app.teams.views import TeamOwnershipMixin

from . import forms, models


class MediaCollectionTable(django_tables2.Table):
    processed = django_tables2.Column(orderable=False, empty_values=(), verbose_name="")
    name = django_tables2.Column(orderable=False)
    operations = django_tables2.Column(orderable=False, empty_values=(), verbose_name="")

    class Meta:
        model = models.TeamMediaCollection
        fields = ["processed", "name", "operations"]

    def render_processed(self, value, record):
        return render_to_string(
            "components/media_progress.html",
            {
                "progress_url": reverse("media:progress", kwargs={"pk": record.id}),
                "processed_time": record.processed_time,
            },
        )

    def render_operations(self, value, record):
        operations = ['<div class="text-right">']

        update_url = reverse("media:form_update", kwargs={"pk": record.id})
        operations.append(
            f'<a class="btn btn-primary px-4 py-2" title="Edit" href="{update_url}">'
            + '<i class="bx bx-edit"></i>'
            + "</a>"
        )
        remove_url = reverse("media:remove", kwargs={"pk": record.id})
        operations.append(
            f'<a class="btn btn-primary ms-2 px-4 py-2" title="Remove" href="{remove_url}">'
            + '<i class="bx bx-trash-alt"></i>'
            + "</a>"
        )

        operations.append("</div>")
        return format_html("".join(operations))


class ListView(TeamOwnershipMixin, TemplateView):
    template_name = "media_list.html"
    model = models.TeamMediaCollection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context["collection_count"] = kwargs["count"]
        context["collections"] = MediaCollectionTable(queryset)

        # context["help_title"] = "Media Collection Help"
        # context["help_body"] = render_to_string("media_help.html")
        return context

    def dispatch(self, request, *args, **kwargs):
        create_redirect = self._initialize_team(request)
        if create_redirect:
            return create_redirect

        queryset = self.get_queryset()
        kwargs["count"] = queryset.count()
        kwargs["disable_check_team"] = True

        if not kwargs["count"]:
            return redirect("media:form_create")

        return super().dispatch(request, *args, **kwargs)


class FormMixin(TeamOwnershipMixin):
    template_name = "media_form.html"
    model = models.TeamMediaCollection
    form_class = forms.MediaCollectionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["team"] = self.team
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["files"] = forms.MediaCollectionFileFormSet(
                self.request.POST, self.request.FILES, instance=self.object, prefix="files"
            )
            context["bookmarks"] = forms.MediaCollectionBookmarkFormSet(
                self.request.POST, instance=self.object, prefix="bookmarks"
            )
        else:
            context["files"] = forms.MediaCollectionFileFormSet(instance=self.object, prefix="files")
            context["bookmarks"] = forms.MediaCollectionBookmarkFormSet(instance=self.object, prefix="bookmarks")

        queryset = self.get_queryset()
        context["collection_count"] = queryset.count()

        # context["help_title"] = "Media Collection Help"
        # context["help_body"] = render_to_string("media_help.html")

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        files = context["files"]
        bookmarks = context["bookmarks"]

        with transaction.atomic():
            form.instance.team = self.team
            self.object = form.save()

            if files.is_valid() and bookmarks.is_valid():
                files.instance = self.object
                files.save()

                bookmarks.instance = self.object
                bookmarks.save()

                self.object.create_event()
            else:
                return self.render_to_response(context)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("media:list")


class CreateFormView(FormMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "create"
        return context


class UpdateFormView(FormMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "update"
        return context


class RemoveView(TeamOwnershipMixin, DeleteView):
    template_name = "media_confirm_delete.html"
    model = models.TeamMediaCollection

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self, **kwargs):
        return reverse("media:list")
