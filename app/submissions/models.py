from django.db import models
from django.utils.translation import gettext_lazy as _

from app.utils import fields as model_fields
from app.utils.models import BaseUUIDModel
from app.events.models import Event


class TextEmbedding(BaseUUIDModel):
    text = models.TextField(_("Text"), blank=False)
    embeddings = model_fields.ListField(_("Embeddings"))

    def __str__(self):
        return "[ {} ]: {}".format(self.id, self.text)

    def create_event(self, operation="update"):
        Event.objects.create(
            type="form_embedding",
            data={
                "operation": operation,
                "id": str(self.id),
                "text": self.text,
                "embeddings": self.embeddings,
            },
        )


class FormSubmission(BaseUUIDModel):
    session_id = models.CharField(_("Session ID"), blank=False, max_length=50)
    path = models.CharField(_("Path"), blank=False, max_length=1024)
    name = models.CharField(_("Name"), blank=False, max_length=255)
    fields = model_fields.DictionaryField(_("Fields"))

    nav_path = models.CharField(_("Navigation Path"), blank=True, null=True, max_length=1024)
    page = model_fields.DictionaryField(_("Page Definition"))

    def __str__(self):
        return self.name

    def create_event(self, operation="update"):
        Event.objects.create(
            type="form_submission",
            data={
                "operation": operation,
                "id": str(self.id),
                "session_id": self.session_id,
                "path": self.path,
                "name": self.name,
                "fields": self.fields,
                "nav_path": self.nav_path,
                "page": self.page,
            },
        )
        if operation != "delete":
            self.save()
