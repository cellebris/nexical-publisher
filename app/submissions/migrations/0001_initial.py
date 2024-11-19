# Generated by Django 5.0.7 on 2024-11-19 07:18

import app.utils.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FormSubmission",
            fields=[
                ("created", models.DateTimeField(editable=False)),
                ("updated", models.DateTimeField(editable=False)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid1, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                ("fields", app.utils.fields.DictionaryField(default=dict, verbose_name="Fields")),
            ],
            options={
                "ordering": ["-created"],
                "abstract": False,
            },
        ),
    ]
