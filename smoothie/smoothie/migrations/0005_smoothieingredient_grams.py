# Generated by Django 4.2 on 2023-04-21 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smoothie', '0004_remove_smoothie_rating_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='smoothieingredient',
            name='grams',
            field=models.FloatField(default=0),
        ),
    ]
