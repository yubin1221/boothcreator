import uuid

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from capability.models import Capability, Capability_Data


# Create your views here.
@csrf_exempt
def capabilityList(request):
    if request.method == 'GET':
        capability_list = Capability.objects.all()
        context = {'list': capability_list, 'category': 'capability'}
        return render(request, 'list2.html', context)
    if request.method == 'POST':
        Capability.objects.create(id=uuid.uuid4(), key=request.POST['key'], 
                                  super_permission=request.POST['super_permission'],
                                  user_permission=request.POST['user_permission'],
                                  is_object=request.POST['is_object'],
                                  is_array=request.POST['is_array'],
                                  is_object_array=request.POST['is_object_array']).save()
        capability_list = Capability.objects.all()
        context = {'list': capability_list, 'category': 'capability'}
        return render(request, 'list2.html', context)

@csrf_exempt
def capabilityInfo(request, capability_id):
    if request.method == 'GET':
        capability = Capability.objects.filter(id=capability_id)
        capability = capability.get()
        data_list = Capability_Data.objects.filter(capability_id=capability_id)
        context = {'category': 'capability', 'sub_category': 'data', 'element': capability,
                   'data_list': data_list}
        return render(request, 'capabilityviewer.html', context)

    if request.method == 'POST':
        capability = Capability.objects.filter(id=capability_id)
        capability = capability.get()
        if request.POST['key'] == '':
            new_key = capability.key
        else:
            new_key = request.POST['key']
        if request.POST['super_permission'] == '':
            new_super_permission = capability.super_permission
        else:
            new_super_permission = request.POST['super_permission']
        if request.POST['user_permission'] == '':
            new_user_permission = capability.user_permission
        else:
            new_user_permission = request.POST['user_permission']
        if request.POST['is_object'] == '':
            new_is_object = capability.is_object
        else:
            new_is_object = request.POST['is_object']
        if request.POST['is_array'] == '':
            new_is_array = capability.is_array
        else:
            new_is_array = request.POST['is_array']
        if request.POST['is_object_array'] == '':
            new_is_object_array = capability.is_object_array
        else:
            new_is_object_array = request.POST['is_object_array']
        Capability.objects.filter(id=capability_id).update(
            key=new_key, super_permission=new_super_permission, user_permission=new_user_permission,is_object=new_is_object,
            is_array=new_is_array, is_object_array=new_is_object_array)
        data_list = Capability_Data.objects.filter(capability_id=capability_id)

        capability = Capability.objects.filter(id=capability_id)
        capability = capability.get()
        context = {'category': 'capability', 'sub_category': 'data', 'element': capability, 'data_list': data_list}
        return render(request, 'capabilityviewer.html', context)
    if request.method == 'DELETE':
        Capability.objects.filter(id=capability_id).delete()
        return redirect('../')


@csrf_exempt
def device_data(request, device_id):
    if request.method == 'GET':
        device_data_list = Device_Data.objects.filter(device_id=device_id)
        data_list = Data.objects.all()
        context = {'category': 'device', 'sub_category': 'data', 'included_list': device_data_list,
                   'sub_list': data_list}
        return render(request, 'devicedataviewer.html', context)
    if request.method == 'POST':
        if Data.objects.filter(id=request.POST['id']).exists():
            device = Device.objects.filter(id=device_id).get()
            data = Data.objects.filter(id=request.POST['id']).get()
            Device_Data.objects.create(device=device, data=data).save()
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
