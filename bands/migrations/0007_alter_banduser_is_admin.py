# Generated by Django 4.2.2 on 2023-07-03 00:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bands", "0006_alter_band_is_archived_alter_banduser_is_admin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="banduser",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
    ]
