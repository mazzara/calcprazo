from django.urls import path, re_path

app_name = 'calc'

urlpatterns = [
 path('', HomeCalc.as_view(), name='home'),
]