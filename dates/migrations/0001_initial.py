# Generated by Django 4.2.2 on 2023-07-07 22:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("venues", "0001_initial"),
        ("contacts", "0001_initial"),
        ("tours", "0001_initial"),
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Date",
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
                ("date", models.DateField()),
                ("title", models.CharField(blank=True, max_length=255)),
                ("notes", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("UNCONFIRMED", "UNCONFIRMED"),
                            ("INQUIRY SENT", "INQUIRY SENT"),
                            ("HOLD", "HOLD"),
                            ("OFFER RECEIVED", "OFFER RECEIVED"),
                            ("CONFIRMED", "CONFIRMED"),
                        ],
                        default="UNCONFIRMED",
                        max_length=30,
                    ),
                ),
                ("hold", models.IntegerField(default=None, null=True)),
                (
                    "contacts",
                    models.ManyToManyField(related_name="dates", to="contacts.contact"),
                ),
                (
                    "place",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="dates",
                        to="places.place",
                    ),
                ),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dates",
                        to="tours.tour",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
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
                ("deal", models.TextField(default="")),
                ("hospitality", models.TextField(default="")),
                ("notes", models.TextField(default="")),
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
        migrations.CreateModel(
            name="LogEntry",
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
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("note", models.TextField(default="")),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dates.date"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="date",
            name="venues",
            field=models.ManyToManyField(
                related_name="dates", through="dates.Show", to="venues.venue"
            ),
        ),
    ]
