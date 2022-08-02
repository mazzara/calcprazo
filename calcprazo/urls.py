from django.urls import path, re_path
from .views import HomeCalc

app_name = 'calcprazo'

urlpatterns = [
 path('', HomeCalc, name='home'),
]