# Generated by Django 4.1 on 2022-08-04 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calcprazo", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="calculaprazo",
            name="contagem_em_dias_uteis",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="calculaprazo",
            name="dia_util",
            field=models.IntegerField(default=0),
        ),
    ]
