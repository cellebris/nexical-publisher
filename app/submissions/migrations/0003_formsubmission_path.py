# Generated by Django 5.0.7 on 2024-11-20 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0002_formsubmission_session_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="formsubmission",
            name="path",
            field=models.CharField(default="", max_length=1024, verbose_name="Path"),
            preserve_default=False,
        ),
    ]
