# Generated by Django 4.2.2 on 2023-07-07 22:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("dates", "0001_initial"),
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Timeslot",
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
                ("title", models.CharField(blank=True, default="", max_length=255)),
                ("type", models.CharField(max_length=25)),
                ("details", models.TextField(blank=True, default="")),
                ("start_time", models.TimeField(blank=True, null=True)),
                ("start_after_midnight", models.BooleanField(default=False)),
                ("end_time", models.TimeField(blank=True, null=True)),
                ("end_after_midnight", models.BooleanField(default=False)),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="timeslots",
                        to="dates.date",
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="timeslot_destinations",
                        to="places.place",
                    ),
                ),
                (
                    "origin",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="timeslot_origins",
                        to="places.place",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
