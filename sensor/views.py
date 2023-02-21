import uuid

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from capability.models import Capability
from .models import Sensor, Sensor_Capability


# Create your views here.


@csrf_exempt
def sensorList(request):
    if request.method == 'GET':
        sensor_list = Sensor.objects.all()
        context = {'list': sensor_list, 'category': 'sensor'}
        return render(request, 'list.html', context)
    if request.method == 'POST':
        Sensor.objects.create(id=uuid.uuid4(), name=request.POST['name'], version=request.POST['version'],
                              vendor=request.POST['vendor']).save()
        sensor_list = Sensor.objects.all()
        context = {'list': sensor_list, 'category': 'sensor'}
        return render(request, 'list.html', context)


@csrf_exempt
def sensorInfo(request, sensor_id):
    if request.method == 'GET':
        sensor = Sensor.objects.filter(id=sensor_id)
        sensor = sensor.get()
        capability_list = Sensor_Capability.objects.filter(sensor_id=sensor_id)
        context = {'category': 'sensor', 'sub_category': 'sensor', 'element': sensor,
                   'capability_list': capability_list}
        return render(request, 'sensorviewer.html', context)

    if request.method == 'POST':
        sensor = Sensor.objects.filter(id=sensor_id)
        sensor = sensor.get()
        if request.POST['name'] == '':
            new_name = sensor.name
        else:
            new_name = request.POST['name']
        if request.POST['version'] == '':
            new_version = sensor.version
        else:
            new_version = request.POST['version']
        if request.POST['vendor'] == '':
            new_vendor = sensor.vendor
        else:
            new_vendor = request.POST['vendor']
        Sensor.objects.filter(id=sensor_id).update(name=new_name, version=new_version, vendor=new_vendor)
        capability_list = Sensor_Capability.objects.filter(sensor_id=sensor_id)
        sensor = Sensor.objects.filter(id=sensor_id)
        sensor = sensor.get()
        context = {'category': 'sensor', 'sub_category': 'sensor', 'element': sensor,
                   'capability_list': capability_list}
        return render(request, 'sensorviewer.html', context)
    if request.method == 'DELETE':
        Sensor.objects.filter(id=sensor_id).delete()
        return redirect('../')


@csrf_exempt
def sensor_capability(request, sensor_id):
    if request.method == 'GET':
        sensor_capability_list = Sensor_Capability.objects.filter(sensor_id=sensor_id)
        capability_list = Capability.objects.all()
        context = {'category': 'sensor', 'sub_category': 'capability', 'included_list': sensor_capability_list,
                   'sub_list': capability_list}
        return render(request, 'sensorcapabilityviewer.html', context)
    if request.method == 'POST':
        if Capability.objects.filter(id=request.POST['id']).exists():
            sensor = Sensor.objects.filter(id=sensor_id).get()
            capability = Capability.objects.filter(id=request.POST['id']).get()
            Sensor_Capability.objects.create(sensor=sensor, capability=capability).save()
            return redirect('./')
        return redirect('./')


@csrf_exempt
def sensor_capability_del(request, sensor_id, capability_id):
    if request.method == 'GET':
        capability=Capability.objects.filter(id=capability_id).get()
        context={'element': capability}
        return render(request, 'sensorcapabilitydel.html', context)
    if request.method == 'DELETE':
        sensor = Sensor.objects.filter(id=sensor_id).get()
        capability = Capability.objects.filter(id=capability_id).get()
        Sensor_Capability.objects.filter(sensor=sensor, capability=capability).delete()
        return redirect('../')
