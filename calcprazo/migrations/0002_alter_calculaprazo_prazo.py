# Generated by Django 4.0.5 on 2022-08-02 05:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcprazo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculaprazo',
            name='prazo',
            field=models.IntegerField(default=15, validators=[django.core.validators.MaxValueValidator(600), django.core.validators.MinValueValidator(1)]),
        ),
    ]