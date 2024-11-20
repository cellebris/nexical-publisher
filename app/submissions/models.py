from django.db import models
from django.utils.translation import gettext_lazy as _

from app.utils import fields
from app.utils.models import BaseUUIDModel
from app.events.models import Event


class FormSubmission(BaseUUIDModel):
    session_id = models.CharField(_("Session ID"), blank=False, max_length=50)
    name = models.CharField(_("Name"), blank=False, max_length=255)
    fields = fields.DictionaryField(_("Fields"))

    def __str__(self):
        return self.name

    def create_event(self, operation="update"):
        Event.objects.create(
            type="form_submission",
            data={
                "operation": operation,
                "id": str(self.id),
                "session_id": self.session_id,
                "name": self.name,
                "fields": self.fields
            },
        )
        if operation != "delete":
            self.save()
