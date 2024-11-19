# Generated by Django 4.2.5 on 2024-05-22 05:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0001_initial"),
        ("projects", "0004_remove_teamproject_summary_prompt_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="teamproject",
            name="documents",
            field=models.ManyToManyField(blank=True, related_name="projects", to="documents.teamdocumentcollection"),
        ),
        migrations.AlterField(
            model_name="teamproject",
            name="summary_model",
            field=models.CharField(
                choices=[("mixtral_di_7bx8", "Mixtral 8x7b (Default)")],
                default="mixtral_di_7bx8",
                max_length=60,
                verbose_name="Summarization Model",
            ),
        ),
    ]