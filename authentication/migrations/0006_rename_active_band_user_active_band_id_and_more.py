# Generated by Django 4.2.2 on 2023-07-04 18:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0005_alter_user_active_band_alter_user_active_tour"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="active_band",
            new_name="active_band_id",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="active_tour",
            new_name="active_tour_id",
        ),
    ]
