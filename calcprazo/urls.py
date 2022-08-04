from django.urls import path, re_path
from calcprazo import views

app_name = 'calcprazo'

urlpatterns = [
    path('', views.homeCalc, name='home'),
    path('login/', views.LoginView.as_view(), name='view_login'),
    path('logout/', views.LogoutView.as_view(), name='view_logout'),
    path('signup/', views.SignupView.as_view(), name='view_signup'),
    path('calculadora/', views.CalculateView.as_view(), name='calculate_view'),
    path('get-calc-data/', views.getCalcDate, name='get-calc-data'),
    path('memoria-de-calculo/', views.CalculateList.as_view(), name='memoria-de-calculo'),
    path('feriados/', views.FeriadosView.as_view(), name='feriados'),
    path('ajax_delete_feriado/', views.feriadoDelete, name='ajax_delete_feriado'),
    path('ajax_delete_calculo/', views.calculoDelete, name='ajax_delete_calculo'),
    path('ajax_add_feriado/', views.feriadoAdd, name='ajax_add_feriado'),
    path('ajax_get_feriado/', views.getFeriado, name='ajax_get_feriado'),
    path('ajax_get_calculo/', views.getCalculo, name='ajax_get_calculo'),
    path('ajax_update_calculo/', views.calculoUpdate, name='ajax_update_calculo'),
]