from datetime import datetime
from rest_framework.decorators import action
from rest_framework import status, fields, serializers
from rest_framework.response import Response

from app.api import permissions, views

from . import models

import time


#
# Update Handler
#
def create_form_event(self, instance):
    if not instance.page:
        instance.create_event()


def create_embedding_event(self, instance):
    if not instance.embeddings:
        instance.create_event()
        start_time = datetime.now()
        while (datetime.now() - start_time).seconds < 100:
            embedding_test = models.TextEmbedding.objects.get(id=instance.id)
            if embedding_test.embeddings:
                instance.embeddings = embedding_test.embeddings
                break
            time.sleep(0.5)


#
# Model Endpoints
#
views.generate(
    models.TextEmbedding,
    permission_classes=[permissions.EnginePermissions],
    filter_fields={
        "id": "id",
        "text": "long_text",
        "created": "date_time",
        "updated": "date_time",
    },
    ordering_fields=["created"],
    search_fields=["text"],
    view_fields=[
        "id",
        "text",
        "embeddings",
        "created",
        "updated",
    ],
    create_fields=[
        "text",
        ("embeddings", {"read_only": True}),
    ],
    update_fields=[
        "embeddings",
    ],
    handler=create_embedding_event,
)


views.generate(
    models.FormSubmission,
    permission_classes=[permissions.EnginePermissions],
    filter_fields={
        "id": "id",
        "session_id": "id",
        "path": "short_text",
        "name": "short_text",
        "nav_path": "short_text",
        "created": "date_time",
        "updated": "date_time",
    },
    ordering_fields=["created", "name", "session_id", "path", "nav_path"],
    search_fields=["name", "session_id", "path", "nav_path"],
    view_fields=[
        "id",
        "session_id",
        "path",
        "name",
        "fields",
        "nav_path",
        "page",
        "created",
        "updated",
    ],
    create_fields=[
        "session_id",
        "path",
        "nav_path",
        "name",
        "fields",
    ],
    update_fields=[
        "page",
    ],
    handler=create_form_event,
)
