# Generated by Django 3.2.3 on 2021-05-21 23:11

import core.models
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=core.models.LatitudeField(blank=True, decimal_places=7, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=core.models.LongitudeField(blank=True, decimal_places=7, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='Долгота'),
        ),
    ]