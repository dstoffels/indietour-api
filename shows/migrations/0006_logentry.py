# Generated by Django 4.2.2 on 2024-01-22 03:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("shows", "0005_alter_show_status_delete_status"),
    ]

    operations = [
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
                        on_delete=django.db.models.deletion.CASCADE, to="shows.show"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
