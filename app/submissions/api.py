from app.api import permissions, serializers, views

from . import models


#
# Update Handler
#
def create_form_event(self, instance):
    instance.create_event()


#
# Model Endpoints
#
views.generate(
    models.FormSubmission,
    permission_classes=[permissions.EnginePermissions],
    filter_fields={
        "id": "id",
        "name": "short_text",
        "created": "date_time",
        "updated": "date_time"
    },
    ordering_fields=["name"],
    search_fields=["name"],
    view_fields=[
        "id",
        "name",
        "created",
        "updated",
        "fields"
    ],
    save_fields=[
        "name",
        "fields",
    ],
    handler=create_form_event,
)
