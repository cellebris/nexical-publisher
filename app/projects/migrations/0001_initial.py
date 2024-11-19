# Generated by Django 4.2.5 on 2024-05-19 20:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("teams", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TeamProject",
            fields=[
                ("created", models.DateTimeField(editable=False)),
                ("updated", models.DateTimeField(editable=False)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid1, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Project Name")),
                ("summary_prompt", models.TextField(default="", verbose_name="Summarization instructions")),
                (
                    "format_prompt",
                    models.TextField(
                        default="\nGenerate an engaging summary on the topic with appropriate headings, subheadings, paragraphs, and bullet points.\n    ",
                        verbose_name="Format instructions",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="projects", to="teams.team"
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
                "abstract": False,
            },
        ),
    ]