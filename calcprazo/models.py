from django.db import models
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Feriado(models.Model):
    FERIADO = 'F'
    PROVIMENTO = 'P'
    INDISPONIBILIDADE = 'I'
    SUSPENDE = [ 
        (FERIADO, 'Feriado'),
        (PROVIMENTO, 'Provimento'),
        (INDISPONIBILIDADE, 'Indisponibilidade'),
    ]

    data_feriado = models.DateField(),
    feriado = models.CharField(max_length=254),
    provimento = models.CharField(max_length=1, choices=SUSPENDE, default=FERIADO)




class CalculaPrazo(models.Model):
    data_stamp = models.DateTimeField(auto_now_add=True, editable=False)
    data_evento = models.DateField()
    evento = models.CharField(max_length=254)
    prazo = models.IntegerField(default=15)
    dias_corridos = models.DateField()
    dias_uteis_banco = models.DateField()
    dias_uteis_tribunal = models.DateField()
    tribunal = models.CharField(max_length=254, null=True, blank=True)
    adv_email = models.EmailField()


# class CoolModelBro(Model):
#     limited_integer_field = IntegerField(
#         default=1,
#         validators=[
#             MaxValueValidator(100),
#             MinValueValidator(1)
#         ]
#      )