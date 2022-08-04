from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import CreateView
from calcprazo import models
from calcprazo.forms import SingupForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from datetime import datetime, timedelta
import json
from django.views.generic import ListView
from django.db import IntegrityError

# Create your views here.
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"
    
    def get_success_url(self):
        return reverse_lazy("calcprazo:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)

class LogoutView(RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class SignupView(CreateView):
    model = models.User
    form_class = SingupForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('calcprazo:view_login')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        email = request.POST.get('email')

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email= email
            new_user.save()
            
            return HttpResponseRedirect(self.get_success_url())

        else:

            return self.render_to_response(self.get_context_data(form=form))

@login_required
def homeCalc(request):
    return redirect('calcprazo:calculate_view')

@method_decorator(login_required, name='dispatch')
class CalculateList(ListView):
    model = models.CalculaPrazo
    template_name = "home/memoria-calculo.html"

    def get_context_data(self, **kwargs):
        context = super(CalculateList, self).get_context_data(**kwargs)
        calculateList = models.CalculaPrazo.objects.all()
        context['calculateList'] = calculateList
        
        return context

@method_decorator(login_required, name='dispatch')
class FeriadosView(ListView):
    model = models.Feriado
    template_name = "home/feriado.html"

    def get_context_data(self, **kwargs):
        context = super(FeriadosView, self).get_context_data(**kwargs)
        feriados = models.Feriado.objects.all()
        context['feriados'] = feriados
        
        return context

@login_required
def feriadoDelete(request):
    if request.method == "POST":
        feriado_id = request.POST.get('feriado_id')
        feriado = models.Feriado.objects.get(id=feriado_id)
        feriado.delete()

        return JsonResponse({'status': 'ok'})

@login_required
def calculoDelete(request):
    if request.method == "POST":
        calculo_id = request.POST.get('calculo_id')
        calculo = models.CalculaPrazo.objects.get(id=calculo_id)
        calculo.delete()

        return JsonResponse({'status': 'ok'})

@login_required
def feriadoAdd(request):
    if request.method == "POST":
        feriadoid = request.POST.get('feriadoid')
        feriado = request.POST.get('feriado')
        provimento = request.POST.get('provimento')
        dataFeriado = request.POST.get('dataFeriado')

        if feriadoid == "-1":
            try:
                models.Feriado.objects.create(
                    feriado=feriado,
                    data_feriado=dataFeriado,
                    provimento=provimento
                )
                return JsonResponse({
                    "status": "Success",
                    "messages": "Informações do Feriado adicionadas!",
                })
            except IntegrityError as e: 
                print(e)
                return JsonResponse({
                    "status": "Error",
                    "messages": "Feriado Error!"
                })
        else:
            try:
                feriadoData = models.Feriado.objects.get(id=feriadoid)
                feriadoData.feriado = feriado
                feriadoData.data_feriado = dataFeriado
                feriadoData.provimento = provimento
        
                feriadoData.save()

                return JsonResponse({
                    "status": "Success",
                    "messages": "Informações do Feriado atualizadas!",
                })

            except IntegrityError as e: 
                return JsonResponse({
                    "status": "Error",
                    "messages": "Feriado Error!"
                })

@login_required
def calculoUpdate(request):
    if request.method == "POST":
        calculoid = request.POST.get('calculoid')
        evento = request.POST.get('evento')
        prazo = request.POST.get('prazo')
        publisherDate = request.POST.get('publisherDate')
        calendarDate = request.POST.get('calendarDate')
        businessDate = request.POST.get('businessDate')
        businessHolidayDate = request.POST.get('businessHolidayDate')

        weekName = datetime.strptime(publisherDate,'%Y-%m-%d')
        conWeekName = convertWeekName(weekName.strftime('%A'))
        weekNum = int(weekName.strftime('%w')) + 1
        
        pubDate = (datetime.strptime(publisherDate,'%Y-%m-%d')).date()
        restDayCount = findFeriadoDay(pubDate, int(prazo) - 1)
        dia_util = (datetime.strptime(businessDate,'%Y-%m-%d') - datetime.strptime(publisherDate,'%Y-%m-%d')).days + 1
        contagem_em_dias_uteis = (datetime.strptime(businessHolidayDate,'%Y-%m-%d') - datetime.strptime(publisherDate,'%Y-%m-%d')).days + 1
        print(calculoid, "fdfdfd")
        if calculoid != "-1":
            try:
                calculoData = models.CalculaPrazo.objects.get(id=calculoid)
                calculoData.evento = evento
                calculoData.prazo = prazo
                calculoData.data_evento = publisherDate
                calculoData.feriado = restDayCount
                calculoData.dia_da_semana = conWeekName
                calculoData.aia_da_semana_num = weekNum
                calculoData.dias_corridos = calendarDate
                calculoData.dias_uteis_banco = businessDate
                calculoData.dias_uteis_tribunal = businessHolidayDate
                calculoData.dia_util = dia_util
                calculoData.contagem_em_dias_uteis = contagem_em_dias_uteis
                calculoData.adv_email=request.user.email

                calculoData.save()

                return JsonResponse({
                    "status": "Success",
                    "messages": "Informações do Calculo atualizadas!",
                })
            except IntegrityError as e: 
                print(e)
                return JsonResponse({
                    "status": "Error",
                    "messages": "Calculo Error!"
                })

@login_required
def getFeriado(request):
    if request.method == "POST":
        feriadoid = request.POST.get('feriadoid')
        feriadoData = models.Feriado.objects.get(id=feriadoid)
        data = {
            'feriado': feriadoData.feriado,
            'provimento': feriadoData.provimento,
            'dataFeriado': feriadoData.data_feriado.strftime('%Y-%m-%d'),
        }
        return JsonResponse(data)

@login_required
def getCalculo(request):
    if request.method == "POST":
        calculoid = request.POST.get('calculoid')
        print(calculoid)
        calculoData = models.CalculaPrazo.objects.get(id=calculoid)
        data = {
            'evento': calculoData.evento,
            'prazo': calculoData.prazo,
            'publisherDate': calculoData.data_evento.strftime('%Y-%m-%d'),
            'calendarDate': calculoData.dias_corridos.strftime('%Y-%m-%d'),
            'businessDate': calculoData.dias_uteis_banco.strftime('%Y-%m-%d'),
            'businessHolidayDate': calculoData.dias_uteis_tribunal.strftime('%Y-%m-%d'),
            
        }
        return JsonResponse(data)

def convertWeekName(weekName):
    if weekName == "Monday":
        conWeekName = "segunda-feira"
    elif weekName == "Tuesday":
       conWeekName = "terça-feira" 
    elif weekName == "Wednesday":
       conWeekName = "quarta-feira" 
    elif weekName == "Thursday":
       conWeekName = "quinta-feira" 
    elif weekName == "Friday":
       conWeekName = "sexta-feira" 
    elif weekName == "Saturday":
       conWeekName = "sábado" 
    elif weekName == "Sunday":
       conWeekName = "domingo" 

    return conWeekName

@method_decorator(login_required, name='dispatch')
class CalculateView(CreateView):
    model = models.CalculaPrazo
    fields = "__all__"
    template_name = "home/calculator.html"

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            evento = request.POST.get('evento')
            publisherDate = request.POST.get('publisherDate')
            prazo = request.POST.get('prazo')
            calendarDate = request.POST.get('calendarDate')
            businessDate = request.POST.get('businessDate')
            businessHolidayDate = request.POST.get('businessHolidayDate')

            weekName = datetime.strptime(publisherDate,'%Y-%m-%d')
            conWeekName = convertWeekName(weekName.strftime('%A'))
            weekNum = int(weekName.strftime('%w')) + 1
            
            pubDate = (datetime.strptime(publisherDate,'%Y-%m-%d')).date()
            restDayCount = findFeriadoDay(pubDate, int(prazo) - 1)
            dia_util = (datetime.strptime(businessDate,'%Y-%m-%d') - datetime.strptime(publisherDate,'%Y-%m-%d')).days + 1
            contagem_em_dias_uteis = (datetime.strptime(businessHolidayDate,'%Y-%m-%d') - datetime.strptime(publisherDate,'%Y-%m-%d')).days + 1
            models.CalculaPrazo.objects.create(
                data_evento=publisherDate,
                evento=evento,
                prazo=prazo,
                feriado=restDayCount,
                dia_da_semana = conWeekName,
                aia_da_semana_num = weekNum,
                dias_corridos=calendarDate,
                dias_uteis_banco=businessDate,
                dias_uteis_tribunal=businessHolidayDate,
                dia_util = dia_util,
                contagem_em_dias_uteis = contagem_em_dias_uteis,
                adv_email=self.request.user.email
            )

            return HttpResponseRedirect(reverse_lazy('calcprazo:memoria-de-calculo'))

@login_required
def getCalcDate(request):
    if request.method == "POST":
        publisherDate = request.POST.get('publisherDate')
        prazo = request.POST.get('prazo')
        daysToAdd = int(prazo) - 1
        calendarDate = (datetime.strptime(publisherDate,'%Y-%m-%d') + timedelta(daysToAdd)).date()
        pubDate = (datetime.strptime(publisherDate,'%Y-%m-%d')).date()

        findBusiness = findBusinessDay(pubDate, prazo)

        businessDate = findBusiness

        businessHolidayDate = findBusinessHoilDay(pubDate, prazo)
        

        print(calendarDate.weekday(),findBusiness, businessDate, businessHolidayDate)
        data = {
            "calendarDate": calendarDate.strftime('%Y-%m-%d'),
            "businessDate": businessDate.strftime('%Y-%m-%d'),
            "businessHolidayDate": businessHolidayDate.strftime('%Y-%m-%d')
        }

        return JsonResponse(data)

def findBusinessDay(startDate, daysToAdd):
    workingDayCount = 0    
    while workingDayCount <= int(daysToAdd):
        weekday = int(startDate.strftime('%w'))
        feriados = models.Feriado.objects.filter(data_feriado__gte=startDate, data_feriado__lte=startDate, provimento__iexact='F')
        if (weekday != 0 and weekday != 6 and feriados.count() == 0):
            workingDayCount += 1
        if workingDayCount < int(daysToAdd):
            startDate += timedelta(days=1)
    
    return startDate

def findBusinessHoilDay(startDate, daysToAdd):
    workingDayCount = 0    
    while workingDayCount <= int(daysToAdd):
        weekday = int(startDate.strftime('%w'))
        feriados = models.Feriado.objects.filter(data_feriado__gte=startDate, data_feriado__lte=startDate)
        if (weekday != 0 and weekday != 6 and feriados.count() == 0):
            workingDayCount += 1
        if workingDayCount < int(daysToAdd):
            startDate += timedelta(days=1)
    
    return startDate

def findFeriadoDay(startDate, daysToAdd):
    workingDayCount = 0 
    restDayCount = 0   
    while workingDayCount <= int(daysToAdd):
        weekday = int(startDate.strftime('%w'))
        feriados = models.Feriado.objects.filter(data_feriado__gte=startDate, data_feriado__lte=startDate)
        if (weekday != 0 and weekday != 6 and feriados.count() == 0):
            workingDayCount += 1
        else:
            restDayCount += 1
        if workingDayCount < int(daysToAdd):
            startDate += timedelta(days=1)
    
    return restDayCount 