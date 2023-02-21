import uuid

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from attribute.models import Attribute, Attribute_Data
from data.models import Data


# Create your views here.
@csrf_exempt
def attributeList(request):
    if request.method == 'GET':
        attribute_list = Attribute.objects.all()
        context = {'list': attribute_list, 'category': 'attribute'}
        return render(request, 'list2.html', context)
    if request.method == 'POST':
        checkbox_array=request.POST.getlist('array[]')
        Attribute.objects.create(id=uuid.uuid4(), key=request.POST['key'], 
                                  super_permission=request.POST['super_permission'],
                                  user_permission=request.POST['user_permission'],
                                  is_object= "obj" in checkbox_array,
                                  is_array= "array" in checkbox_array,
                                  is_object_array="objarray" in checkbox_array).save()
        attribute_list = Attribute.objects.all()
        context = {'list': attribute_list, 'category': 'attribute'}
        return render(request, 'list2.html', context)

@csrf_exempt
def attributeInfo(request, attribute_id):
    if request.method == 'GET':
        attribute = Attribute.objects.filter(id=attribute_id)
        attribute = attribute.get()
        data_list = Attribute_Data.objects.filter(attribute_id=attribute_id)
        context = {'category': 'attribute', 'sub_category': 'data', 'element': attribute,
                   'data_list': data_list}
        return render(request, 'capabilityviewer.html', context)

    if request.method == 'POST':
        attribute = Attribute.objects.filter(id=attribute_id)
        attribute = attribute.get()
        if request.POST['key'] == '':
            new_key = attribute.key
        else:
            new_key = request.POST['key']
        if request.POST['super_permission'] == '':
            new_super_permission = attribute.super_permission
        else:
            new_super_permission = request.POST['super_permission']
        if request.POST['user_permission'] == '':
            new_user_permission = attribute.user_permission
        else:
            new_user_permission = request.POST['user_permission']
        checkbox_array=request.POST.getlist('array[]')
        Attribute.objects.filter(id=attribute_id).update(
            key=new_key, super_permission=new_super_permission, user_permission=new_user_permission,
            is_object="obj" in checkbox_array,
            is_array="array" in checkbox_array,
            is_object_array="objarray" in checkbox_array)
        data_list = Attribute_Data.objects.filter(attribute_id=attribute_id)

        attribute = Attribute.objects.filter(id=attribute_id)
        attribute = attribute.get()
        context = {'category': 'attribute', 'sub_category': 'data', 'element': attribute, 'data_list': data_list}
        return render(request, 'capabilityviewer.html', context)
    if request.method == 'DELETE':
        Attribute.objects.filter(id=attribute_id).delete()
        return redirect('../')


@csrf_exempt
def attribute_data(request, attribute_id):
    if request.method == 'GET':
        attribute_data_list = Attribute_Data.objects.filter(attribute_id=attribute_id)
        data_list = Data.objects.all()
        context = {'category': 'attribute', 'sub_category': 'data', 'included_list': attribute_data_list,
                   'sub_list': data_list}
        return render(request, 'capabilitydataviewer.html', context)
    if request.method == 'POST':
        if Data.objects.filter(id=request.POST['id']).exists():
            attribute = Attribute.objects.filter(id=attribute_id).get()
            data = Data.objects.filter(id=request.POST['id']).get()
            Attribute_Data.objects.create(attribute=attribute, data=data).save()
            return redirect('./')
        return redirect('./')

@csrf_exempt
def attribute_data_del(request, attribute_id, data_id):
    if request.method == 'GET':
        data=Data.objects.filter(id=data_id).get()
        context={'element': data}
        return render(request, 'capabilitydatadel.html', context)
    if request.method == 'DELETE':
        attribute = Attribute.objects.filter(id=attribute_id).get()
        data = Data.objects.filter(id=data_id).get()
        Attribute_Data.objects.filter(attribute=attribute, data=data).delete()
        return redirect('../')