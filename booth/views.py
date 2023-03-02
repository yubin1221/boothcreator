import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from attribute.models import Attribute, Attribute_Data
from capability.models import Capability, Capability_Data
from connection.models import Connection, Connection_Data
from data.models import Data
from device.models import Device, Device_Sensor, Device_Attribute, Device_Connection
from sensor.models import Sensor, Sensor_Capability
from .models import Booth, Booth_Device


# Create your views here.
@csrf_exempt
def boothList(request):
    if request.method == 'GET':
        booth_list = Booth.objects.all()
        context = {'list': booth_list, 'category': 'booth'}
        return render(request, 'list.html', context)
    if request.method == 'POST':
        Booth.objects.create(id=uuid.uuid4(), name=request.POST['name'], version=request.POST['version']).save()
        booth_list = Booth.objects.all()
        context = {'list': booth_list, 'category': 'booth'}
        return render(request, 'list.html', context)


@csrf_exempt
def boothInfo(request, booth_id):
    if request.method == 'GET':
        device_list = Booth_Device.objects.filter(booth_id=booth_id)
        booth = Booth.objects.filter(id=booth_id)
        booth = booth.get()
        context = {'category': 'booth', 'sub_category': 'device', 'element': booth, 'list': device_list}
        return render(request, 'boothviewer.html', context)

    if request.method == 'POST':
        booth = Booth.objects.filter(id=booth_id)
        booth = booth.get()
        if request.POST['name'] == '':
            new_name = booth.name
        else:
            new_name = request.POST['name']
        if request.POST['version'] == '':
            new_version = booth.version
        else:
            new_version = request.POST['version']
        Booth.objects.filter(id=booth_id).update(name=new_name, version=new_version)
        device_list = Booth_Device.objects.filter(booth_id=booth_id)
        booth = Booth.objects.filter(id=booth_id)
        booth = booth.get()
        context = {'category': 'booth', 'sub_category': 'device', 'element': booth, 'list': device_list}
        return render(request, 'boothviewer.html', context)
    if request.method == 'DELETE':
        Booth.objects.filter(id=booth_id).delete()
        return redirect('../')


@csrf_exempt
def booth_device(request, booth_id):
    booth_device_list = Booth_Device.objects.filter(booth_id=booth_id)
    device_list = Device.objects.all()
    context = {'category': 'booth', 'sub_category': 'device', 'included_list': booth_device_list,
               'sub_list': device_list}
    if request.method == 'POST':
        if Device.objects.filter(id=request.POST['id']).exists():
            booth = Booth.objects.filter(id=booth_id).get()
            device = Device.objects.filter(id=request.POST['id']).get()
            Booth_Device.objects.create(booth=booth, device=device).save()
            return redirect('./')
        return redirect('./')
    return render(request, 'boothdeviceviewer.html', context)

@csrf_exempt
def booth_device_del(request, booth_id, device_id):
    if request.method == 'GET':
        device=Device.objects.filter(id=device_id).get()
        context={'element': device}
        return render(request, 'boothdevicedel.html', context)
    if request.method == 'DELETE':
        booth = Booth.objects.filter(id=booth_id).get()
        device = Device.objects.filter(id=device_id).get()
        Booth_Device.objects.filter(booth=booth, device=device).delete()
        return redirect('../')

@csrf_exempt
def booth_json(request, booth_id):
    booth=Booth.objects.filter(id=booth_id).get()
    response = make_booth_json(booth)
    return JsonResponse(response)



def make_booth_json(booth):
    response_json = {
        'item': {
            'booth': {
                'apiVersion': 'v1',
                'kind': 'Booth',
                'metadata': {
                    'id': booth.id,
                    'name': booth.name,
                    'version': booth.version
                },
                'spec': {
                    'devices':[]
                }

            }
        }
    }
    booth_device=Booth_Device.objects.filter(booth_id=booth.id)
    for booth_device_item in booth_device:
        device=Device.objects.filter(id=booth_device_item.device.id).get()
        response_json['item']['booth']['spec']['devices'].append(
            make_device_json(device)
        )
    return response_json
def make_device_json(device):
    response_json={
        'apiVersion': 'v1',
        'kind': 'Device',
        'metadata': {
            'id': device.id,
            'name': device.name,
            'vendor': device.vendor,
            'version': device.version
        },
        'spec' :{
            'connection':{},
            'attributes' :{},
            'sensors':[]
        }
    }
    device_sensor=Device_Sensor.objects.filter(device_id=device.id)
    for device_sensor_item in device_sensor:
        sensor=Sensor.objects.filter(id=device_sensor_item.sensor.id).get()
        response_json['spec']['sensors'].append(make_sensor_json(sensor))

    device_attribute=Device_Attribute.objects.filter(device_id=device.id)
    for device_attribute_item in device_attribute:

        attribute=Attribute.objects.filter(id=device_attribute_item.attribute.id).get()
        response_json['spec']['attributes'][attribute.key] = make_attribute_json(attribute)

    device_connection=Device_Connection.objects.filter(device_id=device.id)
    for device_connection_itme in device_connection:
        connection=Connection.objects.filter(id=device_connection_itme.connection.id).get()
        response_json['spec']['connection'][connection.key] = make_connection_json(connection)

    return response_json
def make_sensor_json(sensor):

    response_json={
        'apiVersion': 'v1',
        'kind': 'Sensor',
        'metadata': {
            'id': sensor.id,
            'name': sensor.name,
            'vendor': sensor.vendor,
            'version': sensor.version
        },
        'spec': {
            'capabilities': {}
        }
    }
    sensor_capability=Sensor_Capability.objects.filter(sensor_id=sensor.id)
    for sensor_capability_item in sensor_capability:
        #capability=Capability.objects.filter(id=sensor_capability_item.capability.id).get()
        capability = sensor_capability_item.capability
        response_json['spec']['capabilities'][capability.key]=make_capability_json(capability)
    return response_json

def make_capability_json(capability):
    response_json={}
    capability_data=Capability_Data.objects.filter(capability_id=capability.id)
    if not capability.is_array and not capability.is_object and not capability.is_object_array:
        data=Data.objects.filter(id=capability_data.get().data.id).get()

        response_json= {'label_ko': capability.label_ko, 'label_en': capability.label_en, 'primitive': data.primitive,
                        'defaultValue': data.default_value, 'isCategorical': data.is_category,
                        'hasLengthLimit': data.has_length_limit, 'unitOfValue': data.unit_of_value,
                        'userPermission': capability.user_permission, 'superPermission': capability.super_permission,
                        'validator': {
                            'type': data.primitive,
                            'minLength': data.min_length,
                            'maxLength': data.max_length,
                            'format': data.format,
                            'pattern': data.pattern,
                            'minimum': data.minimum,
                            'maximum': data.maximum,
                            'multipleOf': data.multiple_of
                        }}
    elif capability.is_array and not capability.is_object and not capability.is_object_array:
        data=Data.objects.filter(id=capability_data.get().data.id).get()
        response_json ={
            'label_ko': capability.label_ko,
            'label_en': capability.label_en,
            'primitive': 'array',
            'userPermission': capability.user_permission,
            'superPermission': capability.super_permission
        }

        response_json['items']={
            'primitive': data.primitive,
            'defaultValue': data.default_value,
            'isCategorical': data.is_category,
            'hasLengthLimit': data.has_length_limit,
            'unitOfValue': data.unit_of_value,
        }
        response_json['validator']={
            'type': 'array',
            'items': {
                'type': data.primitive,
                'minLength': data.min_length,
                'maxLength': data.max_length,
                'format': data.format,
                'pattern': data.pattern,
                'minimum': data.minimum,
                'maximum': data.maximum,
                'multipleOf': data.multiple_of
            }
        }
    elif not capability.is_array and capability.is_object and not capability.is_object_array:
        data=Data.objects.filter(id=capability_data.get().data.id)
        response_json = {'label_ko': capability.label_ko, 'label_en': capability.label_en, 'primitive': 'object',
                         'userPermission': capability.user_permission, 'superPermission': capability.super_permission,
                         'validator': {
                             'type': 'object',
                             'required': [],
                             'properties': {}
                         }, 'properties': {}}
        for data_item in data:
            response_json['validator']['required'].append(data_item.name)
            response_json['properties'][data_item.name]={
                'primitive': data_item.primitive,
                'defaultValue': data_item.default_value,
                'isCategorical': data_item.is_category,
                'hasLengthLimit': data_item.has_length_limit,
                'unitOfValue': data_item.unit_of_value,
            }

            response_json['validator']['properties'][data_item.name]={
                'type': data_item.type,
                'minLength': data_item.min_length,
                'maxLength': data_item.max_length,
                'format': data_item.format,
                'pattern': data_item.pattern,
                'minimum': data_item.minimum,
                'maximum': data_item.maximum,
                'multipleOf': data_item.multiple_of
            }
    elif not capability.is_array and not capability.is_object and capability.is_object_array:
        data = Data.objects.filter(id=capability_data.get().data.id)
        response_json = {
            'label_ko': capability.label_ko,
            'label_en': capability.label_en,
            'primitive': 'array',
            'userPermission': capability.user_permission,
            'superPermission': capability.super_permission,
            'item': {
                'properties': {}
            }
        }
        response_json['validator'] = {
            'type': 'array',
            'required': [],
            'properties': {}
        }
        for data_item in data:
            response_json['item']['properties'][data_item.name] = {
                'primitive': data_item.primitive,
                'defaultValue': data_item.default_value,
                'isCategorical': data_item.is_category,
                'hasLengthLimit': data_item.has_length_limit,
                'unitOfValue': data_item.unit_of_value,
            }
            response_json['validator']['required'].append(data_item.name)
            response_json['validator']['properties'][data_item.name] = {
                'type': 'object',
                'minLength': data_item.min_length,
                'maxLength': data_item.max_length,
                'format': data_item.format,
                'pattern': data_item.pattern,
                'minimum': data_item.minimum,
                'maximum': data_item.maximum,
                'multipleOf': data_item.multiple_of
            }
    return response_json


def make_attribute_json(attribute):

    response_json={}
    attribute_data=Attribute_Data.objects.filter(attribute_id=attribute.id)
    if not attribute.is_array and not attribute.is_object and not attribute.is_object_array:
        data=Data.objects.filter(id=attribute_data.get().data.id).get()

        response_json= {'label_ko': attribute.label_ko, 'label_en': attribute.label_en, 'primitive': data.primitive,
                        'defaultValue': data.default_value, 'isCategorical': data.is_category,
                        'hasLengthLimit': data.has_length_limit, 'unitOfValue': data.unit_of_value,
                        'userPermission': attribute.user_permission, 'superPermission': attribute.super_permission,
                        'validator': {
                            'type': data.primitive,
                            'minLength': data.min_length,
                            'maxLength': data.max_length,
                            'format': data.format,
                            'pattern': data.pattern,
                            'minimum': data.minimum,
                            'maximum': data.maximum,
                            'multipleOf': data.multiple_of
                        }}
    elif attribute.is_array and not attribute.is_object and not attribute.is_object_array:
        data=Data.objects.filter(id=attribute_data.get().data.id).get()
        response_json ={
            'label_ko': attribute.label_ko,
            'label_en': attribute.label_en,
            'primitive': 'array',
            'userPermission': attribute.user_permission,
            'superPermission': attribute.super_permission
        }

        response_json['items']={
            'primitive': data.primitive,
            'defaultValue': data.default_value,
            'isCategorical': data.is_category,
            'hasLengthLimit': data.has_length_limit,
            'unitOfValue': data.unit_of_value,
        }
        response_json['validator']={
            'type': 'array',
            'items': {
                'type': data.primitive,
                'minLength': data.min_length,
                'maxLength': data.max_length,
                'format': data.format,
                'pattern': data.pattern,
                'minimum': data.minimum,
                'maximum': data.maximum,
                'multipleOf': data.multiple_of
            }
        }
    elif not attribute.is_array and attribute.is_object and not attribute.is_object_array:
        data=Data.objects.filter(id=attribute_data.get().data.id)
        response_json = {'label_ko': attribute.label_ko, 'label_en': attribute.label_en, 'primitive': 'object',
                         'userPermission': attribute.user_permission, 'superPermission': attribute.super_permission,
                         'validator': {
                             'type': 'object',
                             'required': [],
                             'properties': {}
                         }, 'properties': {}}
        for data_item in data:
            response_json['validator']['required'].append(data_item.name)
            response_json['properties'][data_item.name]={
                'primitive': data_item.primitive,
                'defaultValue': data_item.default_value,
                'isCategorical': data_item.is_category,
                'hasLengthLimit': data_item.has_length_limit,
                'unitOfValue': data_item.unit_of_value,
            }

            response_json['validator']['properties'][data_item.name]={
                'type': data_item.primitive,
                'minLength': data_item.min_length,
                'maxLength': data_item.max_length,
                'format': data_item.format,
                'pattern': data_item.pattern,
                'minimum': data_item.minimum,
                'maximum': data_item.maximum,
                'multipleOf': data_item.multiple_of
            }
    elif not attribute.is_array and not attribute.is_object and attribute.is_object_array:
        data = Data.objects.filter(id=attribute_data.get().data.id)
        response_json = {
            'label_ko': attribute.label_ko,
            'label_en': attribute.label_en,
            'primitive': 'array',
            'userPermission': attribute.user_permission,
            'superPermission': attribute.super_permission,
            'item': {
                'properties': {}
            }
        }
        response_json['validator'] = {
            'type': 'array',
            'required': [],
            'properties': {}
        }
        for data_item in data:
            response_json['item']['properties'][data_item.name] = {
                'primitive': data_item.primitive,
                'defaultValue': data_item.default_value,
                'isCategorical': data_item.is_category,
                'hasLengthLimit': data_item.has_length_limit,
                'unitOfValue': data_item.unit_of_value,
            }
            response_json['validator']['required'].append(data_item.name)
            response_json['validator']['properties'][data_item.name] = {
                'type': 'object',
                'minLength': data_item.min_length,
                'maxLength': data_item.max_length,
                'format': data_item.format,
                'pattern': data_item.pattern,
                'minimum': data_item.minimum,
                'maximum': data_item.maximum,
                'multipleOf': data_item.multiple_of
            }
    return response_json

def make_connection_json(connection):
    response_json={}
    connection_data=Connection_Data.objects.filter(connection_id=connection.id)
    if not connection.is_array and not connection.is_object and not connection.is_object_array:
        data=Data.objects.filter(id=connection_data.get().data.id).get()

        response_json= {'label_ko': connection.label_ko, 'label_en': connection.label_en, 'primitive': data.primitive,
                        'defaultValue': data.default_value, 'isCategorical': data.is_category,
                        'hasLengthLimit': data.has_length_limit, 'unitOfValue': data.unit_of_value,
                        'userPermission': connection.user_permission, 'superPermission': connection.super_permission,
                        'validator': {
                            'type': data.primitive,
                            'minLength': data.min_length,
                            'maxLength': data.max_length,
                            'format': data.format,
                            'pattern': data.pattern,
                            'minimum': data.minimum,
                            'maximum': data.maximum,
                            'multipleOf': data.multiple_of
                        }}
    elif connection.is_array and not connection.is_object and not connection.is_object_array:
        data=Data.objects.filter(id=connection_data.get().data.id).get()
        response_json ={
            'label_ko': connection.label_ko,
            'label_en': connection.label_en,
            'primitive': 'array',
            'userPermission': connection.user_permission,
            'superPermission': connection.super_permission
        }

        response_json['items']={
            'primitive': data.primitive,
            'defaultValue': data.default_value,
            'isCategorical': data.is_category,
            'hasLengthLimit': data.has_length_limit,
            'unitOfValue': data.unit_of_value,
        }
        response_json['validator']={
            'type': 'array',
            'items': {
                'type': data.primitive,
                'minLength': data.min_length,
                'maxLength': data.max_length,
                'format': data.format,
                'pattern': data.pattern,
                'minimum': data.minimum,
                'maximum': data.maximum,
                'multipleOf': data.multiple_of
            }
        }
    elif not connection.is_array and connection.is_object and not connection.is_object_array:
        data=Data.objects.filter(id=connection_data.get().data.id)
        response_json = {'label_ko': connection.label_ko, 'label_en': connection.label_en, 'primitive': 'object',
                         'userPermission': connection.user_permission, 'superPermission': connection.super_permission,
                         'validator': {
                             'type': 'object',
                             'required': [],
                             'properties': {}
                         }, 'properties': {}}
        for data_item in data:
            response_json['validator']['required'].append(data_item.name)
            response_json['properties'][data_item.name]={
                'primitive': data_item.primitive,
                'defaultValue': data_item.default_value,
                'isCategorical': data_item.is_category,
                'hasLengthLimit': data_item.has_length_limit,
                'unitOfValue': data_item.unit_of_value,
            }

            response_json['validator']['properties'][data_item.name]={
                'type': data_item.primitive,
                'minLength': data_item.min_length,
                'maxLength': data_item.max_length,
                'format': data_item.format,
                'pattern': data_item.pattern,
                'minimum': data_item.minimum,
                'maximum': data_item.maximum,
                'multipleOf': data_item.multiple_of
            }
    elif not connection.is_array and not connection.is_object and connection.is_object_array:
        data = Data.objects.filter(id=connection_data.get().data.id)
        response_json = {
            'label_ko': connection.label_ko,
            'label_en': connection.label_en,
            'primitive': 'array',
            'userPermission': connection.user_permission,
            'superPermission': connection.super_permission,
            'item': {
                'properties': {}
            }
        }
        response_json['validator'] = {
            'type': 'array',
            'required': [],
            'properties': {}
        }
        for data_item in data:
            response_json['item']['properties'][data_item.name] = {
                'primitive': data_item.primitive,
                'defaultValue': data_item.default_value,
                'isCategorical': data_item.is_category,
                'hasLengthLimit': data_item.has_length_limit,
                'unitOfValue': data_item.unit_of_value,
            }
            response_json['validator']['required'].append(data_item.name)
            response_json['validator']['properties'][data_item.name] = {
                'type': 'object',
                'minLength': data_item.min_length,
                'maxLength': data_item.max_length,
                'format': data_item.format,
                'pattern': data_item.pattern,
                'minimum': data_item.minimum,
                'maximum': data_item.maximum,
                'multipleOf': data_item.multiple_of
            }
    return response_json