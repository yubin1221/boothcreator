import uuid

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from sensor.models import Sensor
from .models import Device, Device_Sensor, Device_Attribute, Device_Connection
from attribute.models import Attribute
from connection.models import Connection


# Create your views here.
@csrf_exempt
def deviceList(request):
    if request.method == 'GET':
        device_list = Device.objects.all()
        context = {'list': device_list, 'category': 'device'}
        return render(request, 'list.html', context)
    if request.method == 'POST':
        Device.objects.create(id=uuid.uuid4(), name=request.POST['name'], version=request.POST['version'],
                              vendor=request.POST['vendor']).save()
        device_list = Device.objects.all()
        context = {'list': device_list, 'category': 'device'}
        return render(request, 'list.html', context)


@csrf_exempt
def deviceInfo(request, device_id):
    if request.method == 'GET':
        device = Device.objects.filter(id=device_id)
        device = device.get()
        sensor_list = Device_Sensor.objects.filter(device_id=device_id)
        attribute_list = Device_Attribute.objects.filter(device_id=device_id)
        connection_list = Device_Connection.objects.filter(device_id=device_id)
        context = {'category': 'device', 'sub_category': 'sensor', 'element': device, 'sensor_list': sensor_list,
                   'attribute_list': attribute_list, 'connection_list': connection_list}
        return render(request, 'deviceviewer.html', context)

    if request.method == 'POST':
        device = Device.objects.filter(id=device_id)
        device = device.get()
        if request.POST['name'] == '':
            new_name = device.name
        else:
            new_name = request.POST['name']
        if request.POST['version'] == '':
            new_version = device.version
        else:
            new_version = request.POST['version']
        if request.POST['vendor'] == '':
            new_vendor = device.vendor
        else:
            new_vendor = request.POST['vendor']
        Device.objects.filter(id=device_id).update(name=new_name, version=new_version, vendor=new_vendor)
        sensor_list = Device_Sensor.objects.filter(device_id=device_id)
        attribute_list = Device_Attribute.objects.filter(device_id=device_id)
        connection_list = Device_Connection.objects.filter(device_id=device_id)
        device = Device.objects.filter(id=device_id)
        device = device.get()
        context = {'category': 'device', 'sub_category': 'sensor', 'element': device, 'sensor_list': sensor_list,
                   'attribute_list': attribute_list, 'connection_list': connection_list}
        return render(request, 'deviceviewer.html', context)
    if request.method == 'DELETE':
        Device.objects.filter(id=device_id).delete()
        return redirect('../')


@csrf_exempt
def device_sensor(request, device_id):
    if request.method == 'GET':
        device_sensor_list = Device_Sensor.objects.filter(device_id=device_id)
        sensor_list = Sensor.objects.all()
        context = {'category': 'device', 'sub_category': 'sensor', 'included_list': device_sensor_list,
                   'sub_list': sensor_list}
        return render(request, 'devicesensorviewer.html', context)
    if request.method == 'POST':
        if Sensor.objects.filter(id=request.POST['id']).exists():
            device = Device.objects.filter(id=device_id).get()
            sensor = Sensor.objects.filter(id=request.POST['id']).get()
            Device_Sensor.objects.create(device=device, sensor=sensor).save()
            return redirect('./')
        return redirect('./')


@csrf_exempt
def device_attribute(request, device_id):
    if request.method == 'GET':
        device_attribute_list = Device_Attribute.objects.filter(device_id=device_id)
        attribute_list = Attribute.objects.all()
        context = {'category': 'device', 'sub_category': 'attribute', 'included_list': device_attribute_list,
                   'sub_list': attribute_list}
        return render(request, 'deviceattributeviewer.html', context)
    if request.method == 'POST':
        if Attribute.objects.filter(id=request.POST['id']).exists():
            device = Device.objects.filter(id=device_id).get()
            attribute = Attribute.objects.filter(id=request.POST['id']).get()
            Device_Attribute.objects.create(device=device, attribute=attribute).save()
            return redirect('./')
        return redirect('./')


@csrf_exempt
def device_connection(request, device_id):
    if request.method == 'GET':
        device_connection_list = Device_Connection.objects.filter(device_id=device_id)
        connection_list = Connection.objects.all()
        context = {'category': 'device', 'sub_category': 'connection', 'included_list': device_connection_list,
                   'sub_list': connection_list}
        return render(request, 'deviceconnectionviewer.html', context)
    if request.method == 'POST':
        if Connection.objects.filter(id=request.POST['id']).exists():
            device = Device.objects.filter(id=device_id).get()
            connection = Connection.objects.filter(id=request.POST['id']).get()
            Device_Connection.objects.create(device=device, connection=connection).save()
            return redirect('./')
        return redirect('./')

@csrf_exempt
def device_sensor_del(request, device_id, sensor_id):
    if request.method == 'GET':
        sensor=Sensor.objects.filter(id=sensor_id).get()
        context={'element': sensor}
        return render(request, 'devicesensordel.html', context)
    if request.method == 'DELETE':
        device = Device.objects.filter(id=device_id).get()
        sensor = Sensor.objects.filter(id=sensor_id).get()
        Device_Sensor.objects.filter(device=device, sensor=sensor).delete()
        return redirect('../')

@csrf_exempt
def device_attribute_del(request, device_id, attribute_id):
    if request.method == 'GET':
        attribute=Attribute.objects.filter(id=attribute_id).get()
        context={'element': attribute}
        return render(request, 'deviceattributedel.html', context)
    if request.method == 'DELETE':
        device = Device.objects.filter(id=device_id).get()
        attribute = Attribute.objects.filter(id=attribute_id).get()
        Device_Attribute.objects.filter(device=device, attribute=attribute).delete()
        return redirect('../')
@csrf_exempt
def device_connection_del(request, device_id, connection_id):
    if request.method == 'GET':
        connection=Connection.objects.filter(id=connection_id).get()
        context={'element': connection}
        return render(request, 'deviceconnectiondel.html', context)
    if request.method == 'DELETE':
        device = Device.objects.filter(id=device_id).get()
        connection = Connection.objects.filter(id=connection_id).get()
        Device_Connection.objects.filter(device=device, connection=connection).delete()
        return redirect('../')