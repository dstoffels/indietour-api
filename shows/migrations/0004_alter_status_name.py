# Generated by Django 4.2.2 on 2024-01-21 20:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shows", "0003_status_show_hold_show_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="status",
            name="name",
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
