# Generated by Django 4.2.2 on 2023-06-28 02:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dates", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="date",
            name="date",
            field=models.DateField(),
        ),
    ]
