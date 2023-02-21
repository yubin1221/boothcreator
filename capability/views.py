import uuid

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from capability.models import Capability, Capability_Data
from data.models import Data


# Create your views here.
@csrf_exempt
def capabilityList(request):
    if request.method == 'GET':
        capability_list = Capability.objects.all()
        context = {'list': capability_list, 'category': 'capability'}
        return render(request, 'list2.html', context)
    if request.method == 'POST':
        checkbox_array=request.POST.getlist('array[]')
        Capability.objects.create(id=uuid.uuid4(), key=request.POST['key'], 
                                  super_permission=request.POST['super_permission'],
                                  user_permission=request.POST['user_permission'],
                                  is_object= "obj" in checkbox_array,
                                  is_array= "array" in checkbox_array,
                                  is_object_array="objarray" in checkbox_array).save()
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
        checkbox_array=request.POST.getlist('array[]')
        Capability.objects.filter(id=capability_id).update(
            key=new_key, super_permission=new_super_permission, user_permission=new_user_permission,
            is_object="obj" in checkbox_array,
            is_array="array" in checkbox_array,
            is_object_array="objarray" in checkbox_array)
        data_list = Capability_Data.objects.filter(capability_id=capability_id)

        capability = Capability.objects.filter(id=capability_id)
        capability = capability.get()
        context = {'category': 'capability', 'sub_category': 'data', 'element': capability, 'data_list': data_list}
        return render(request, 'capabilityviewer.html', context)
    if request.method == 'DELETE':
        Capability.objects.filter(id=capability_id).delete()
        return redirect('../')


@csrf_exempt
def capability_data(request, capability_id):
    if request.method == 'GET':
        capability_data_list = Capability_Data.objects.filter(capability_id=capability_id)
        data_list = Data.objects.all()
        context = {'category': 'capability', 'sub_category': 'data', 'included_list': capability_data_list,
                   'sub_list': data_list}
        return render(request, 'capabilitydataviewer.html', context)
    if request.method == 'POST':
        if Data.objects.filter(id=request.POST['id']).exists():
            capability = Capability.objects.filter(id=capability_id).get()
            data = Data.objects.filter(id=request.POST['id']).get()
            Capability_Data.objects.create(capability=capability, data=data).save()
            return redirect('./')
        return redirect('./')

@csrf_exempt
def capability_data_del(request, capability_id, data_id):
    if request.method == 'GET':
        data=Data.objects.filter(id=data_id).get()
        context={'element': data}
        return render(request, 'capabilitydatadel.html', context)
    if request.method == 'DELETE':
        capability = Capability.objects.filter(id=capability_id).get()
        data = Data.objects.filter(id=data_id).get()
        Capability_Data.objects.filter(capability=capability, data=data).delete()
        return redirect('../')