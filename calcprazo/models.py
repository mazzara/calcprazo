from django.db import models
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator


# Models for *CALCPRAZO*
#=======================
# Calcprazo is a simple date calculator aimed to be used by local lawers a and legal staff in Sao Paulo / Brazil.
# Provided 2 iputs, a start date, and a delta days, it will compute the *due date* considering local and special non working days.
# User will get the *due date* in 3 output:
# 1. *due date* calculated by simple current delta days, so: March,1,2022(Tue) + 7 days = March,7,2022(Mon)
# 2. *due date* calculated by genaral working days, so:  March,1,2022(Tue) + 7 days = March,10,2022(Thu)
# 3. *due date* same as above, but calculated by general working days, plus special non working days (special cases)


# FERIADO
#---------
# Like a holyddays table in excell, this table stores all HOLYDAYS, 
# and SPECIAL flaged days that should be consider as a non-working day.
class Feriado(models.Model):
    FERIADO = 'F'             # F = General Holidays Flag as by international standard non banking day
    PROVIMENTO = 'P'          # P = Special Non working day as provided by local law
    INDISPONIBILIDADE = 'I'   # I = Non working day due to system malfunction
    SUSPENDE = [ 
        (FERIADO, 'Feriado'),
        (PROVIMENTO, 'Provimento'),
        (INDISPONIBILIDADE, 'Indisponibilidade'),
    ]
    data_feriado = models.DateField()
    feriado = models.CharField(max_length=254)  #Choice: F, P or I as indication of reason for non-workday flag
    provimento = models.CharField(max_length=1, choices=SUSPENDE, default=FERIADO) #Indication of law or reason to consider this day as non-workday


# CALCULAPRAZO
#-------------
#This model tabel logs all calculation requested by useres
class CalculaPrazo(models.Model):
    data_stamp = models.DateTimeField(auto_now_add=True, editable=False)   #timestamp
    data_evento = models.DateField()             #INPUT date set by user as initial date to compute
    evento = models.CharField(max_length=254)    #Event descprition (user input)
    prazo = models.IntegerField(default=15,
            validators=[
            MaxValueValidator(600),
            MinValueValidator(1)
            ]
            )      #Delta days to compute DUE DATE
    dias_corridos = models.DateField()           # Calculated DUE DATE in symple delta days
    dias_uteis_banco = models.DateField()        # Caldulated DUE DATE in symple non-working days (just accounting for F)
    dias_uteis_tribunal = models.DateField()     # Calculated DUE DATE considering non-working days special cases (accounting for F, P and I)
    tribunal = models.CharField(max_length=254, null=True, blank=True)
    adv_email = models.EmailField()              # email log

