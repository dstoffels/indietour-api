# Generated by Django 4.2.2 on 2023-06-27 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0001_initial"),
        ("authentication", "0002_user_active_band_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="active_tour",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="tours.tour",
            ),
        ),
    ]