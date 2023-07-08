# Generated by Django 4.2.2 on 2023-07-08 15:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("dates", "0003_remove_date_venues_delete_show"),
        ("venues", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Show",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("deal", models.TextField(blank=True, default="")),
                ("hospitality", models.TextField(blank=True, default="")),
                ("notes", models.TextField(blank=True, default="")),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shows",
                        to="dates.date",
                    ),
                ),
                (
                    "venue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="venues.venue"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
