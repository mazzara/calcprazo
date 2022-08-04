from django.db import models
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from soupsieve import select

class UserManager(BaseUserManager):

    def _create_user(self, email, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        if not first_name:
            raise ValueError("Users must have an first name")
        if not last_name:
            raise ValueError("Users must have an last name")
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name = first_name,
            last_name = last_name,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email,first_name, last_name, password, False, False, **extra_fields)

    def create_superuser(self,  email, first_name, last_name, password, **extra_fields):
        user = self._create_user( email, first_name, last_name,password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=False)
    email = models.EmailField(blank=True, unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

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
    feriado = models.CharField(max_length=255)  #Choice: F, P or I as indication of reason for non-workday flag
    provimento = models.CharField(max_length=1, choices=SUSPENDE, default=FERIADO) #Indication of law or reason to consider this day as non-workday

    def __str__(self):
        return self.feriado
    class Meta:
        ordering = ['-data_feriado']


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
    dia_da_semana = models.CharField(max_length=255)
    feriado = models.IntegerField(default=0)
    dia_util = models.IntegerField(default=0)
    contagem_em_dias_uteis = models.IntegerField(default=0)
    aia_da_semana_num = models.IntegerField(default=0)
    tribunal = models.CharField(max_length=254, null=True, blank=True)
    adv_email = models.EmailField()              # email log

    def __str__(self):
        return self.evento

    class Meta:
        ordering = ['-data_evento']

