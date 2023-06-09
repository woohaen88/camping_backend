# Generated by Django 4.2.1 on 2023-05-11 04:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("campings", "0002_campground_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="campground",
            name="ev_friendly",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="campground",
            name="pet_friendly",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="campground",
            name="price",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
