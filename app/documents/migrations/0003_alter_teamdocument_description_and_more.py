# Generated by Django 4.2.13 on 2024-06-18 06:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0002_teamdocument_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teamdocument",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="This information can help guide the AI assistants and is always available to the AI when conducting research.  The purpose of this description is to provide context on the content of this document.",
                verbose_name="Document Description",
            ),
        ),
        migrations.AlterField(
            model_name="teamdocumentcollection",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="This information can help guide the AI assistants and is always available to the AI when conducting research.  The purpose of this description is to provide context on the purpose of this document collection.",
                verbose_name="Document Collection Description",
            ),
        ),
    ]