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
        "session_id": "id",
        "name": "short_text",
        "created": "date_time",
        "updated": "date_time"
    },
    ordering_fields=["created", "name", "session_id"],
    search_fields=["name", "session_id"],
    view_fields=[
        "id",
        "session_id",
        "name",
        "created",
        "updated",
        "fields"
    ],
    save_fields=[
        "session_id",
        "name",
        "fields",
    ],
    handler=create_form_event,
)
