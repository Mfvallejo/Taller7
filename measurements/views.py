from .models import Measurement, Threshold, Variable
from django.shortcuts import render, redirect
from .forms import ThresholdForm
from django.contrib.auth.decorators import login_required
import json, requests


def index(request):
    return render(request, 'index.html')

@login_required
def MeasurementList(request):
    queryset = Measurement.objects.all().order_by('-time')[:10]
    context = {
        'measurement_list': queryset
    }
    return render(request, 'Measurement/measurements.html', context)

@login_required
def ThresholdList(request):
    queryset = Threshold.objects.all()
    role = getRole(request)
    context = {
        'threshold_list': queryset,
        'role': role
    }
    print("role= ", role)
    return render(request, 'Threshold/thresholds.html', context)

@login_required
def ThresholdEdit(request, id_threshold):
    threshold = Threshold.objects.get(variable=id_threshold)
    varName = Variable.objects.get(id=id_threshold)
    if request.method == 'GET':
        form = ThresholdForm(instance=threshold)
    else:
        form =ThresholdForm(request.POST, instance=threshold)
        if form.is_valid():
            form.save()
        return redirect('thresholdList')
    role = getRole(request)
    return render(request, 'Threshold/thresholdEdit.html', {'form':form, 'variable':varName.name, 'role': role})

def getRole(request):
    user = request.user
    auth0user = user.social_auth.get(provider="auth0")
    accessToken = auth0user.extra_data['access_token']
    url = "https://isis2503-mfvallejo.auth0.com/userinfo"
    headers = {'authorization': 'Bearer ' + accessToken}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()
    role = userinfo['https://isis2503-mfvallejo:auth0:com/role']
    return (role)

@login_required
def MeasurementPromedio(request, id_measurement):
    suma = 0
    varName = Variable.objects.get(id=id_measurement)
    for e in Measurement.objects.filter(variable=id_measurement).values_list('value', flat=True):
        print(e)
        suma = suma + e
    print(suma)
    print(Measurement.objects.filter(variable=id_measurement).count())
    promedio = suma/Measurement.objects.filter(variable=id_measurement).count()
    role = getRole(request)
    return render(request, 'Measurement/measurementsPromedio.html', {'variable': varName.name, 'promedio':promedio, 'role': role})
