# Generated by Django 4.2.2 on 2023-07-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("prospects", "0002_prospect_hold"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prospect",
            name="hold",
            field=models.IntegerField(default=0),
        ),
    ]