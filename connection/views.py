from django.shortcuts import render

# Create your views here.
import uuid

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from connection.models import Connection, Connection_Data
from data.models import Data


# Create your views here.
@csrf_exempt
def connectionList(request):
    if request.method == 'GET':
        connection_list = Connection.objects.all()
        context = {'list': connection_list, 'category': 'connection'}
        return render(request, 'list2.html', context)
    if request.method == 'POST':
        checkbox_array=request.POST.getlist('array[]')
        Connection.objects.create(id=uuid.uuid4(), key=request.POST['key'],
                                  label_ko=request.POST['label_ko'],
                                  label_en=request.POST['label_en'],
                                  super_permission=request.POST['super_permission'],
                                  user_permission=request.POST['user_permission'],
                                  is_object= "obj" in checkbox_array,
                                  is_array= "array" in checkbox_array,
                                  is_object_array="objarray" in checkbox_array).save()
        connection_list = Connection.objects.all()
        context = {'list': connection_list, 'category': 'connection'}
        return render(request, 'list2.html', context)

@csrf_exempt
def connectionInfo(request, connection_id):
    if request.method == 'GET':
        connection = Connection.objects.filter(id=connection_id)
        connection = connection.get()
        data_list = Connection_Data.objects.filter(connection_id=connection_id)
        context = {'category': 'connection', 'sub_category': 'data', 'element': connection,
                   'data_list': data_list}
        return render(request, 'capabilityviewer.html', context)

    if request.method == 'POST':
        connection = Connection.objects.filter(id=connection_id)
        connection = connection.get()
        if request.POST['key'] == '':
            new_key = connection.key
        else:
            new_key = request.POST['key']
        if request.POST['super_permission'] == '':
            new_super_permission = connection.super_permission
        else:
            new_super_permission = request.POST['super_permission']
        if request.POST['user_permission'] == '':
            new_user_permission = connection.user_permission
        else:
            new_user_permission = request.POST['user_permission']
        if request.POST['label_ko'] == '':
            new_label_ko = connection.label_ko
        else:
            new_label_ko = request.POST['label_ko']
        if request.POST['label_en'] == '':
            new_label_en = connection.label_en
        else:
            new_label_en = request.POST['label_en']
        checkbox_array=request.POST.getlist('array[]')
        Connection.objects.filter(id=connection_id).update(
            key=new_key,
            label_ko=new_label_ko,
            lable_en=new_label_en,
            super_permission=new_super_permission, user_permission=new_user_permission,
            is_object="obj" in checkbox_array,
            is_array="array" in checkbox_array,
            is_object_array="objarray" in checkbox_array)
        data_list = Connection_Data.objects.filter(connection_id=connection_id)

        connection = Connection.objects.filter(id=connection_id)
        connection = connection.get()
        context = {'category': 'connection', 'sub_category': 'data', 'element': connection, 'data_list': data_list}
        return render(request, 'capabilityviewer.html', context)
    if request.method == 'DELETE':
        Connection.objects.filter(id=connection_id).delete()
        return redirect('../')


@csrf_exempt
def connection_data(request, connection_id):
    if request.method == 'GET':
        connection_data_list = Connection_Data.objects.filter(connection_id=connection_id)
        data_list = Data.objects.all()
        context = {'category': 'connection', 'sub_category': 'data', 'included_list': connection_data_list,
                   'sub_list': data_list}
        return render(request, 'capabilitydataviewer.html', context)
    if request.method == 'POST':
        if Data.objects.filter(id=request.POST['id']).exists():
            connection = Connection.objects.filter(id=connection_id).get()
            data = Data.objects.filter(id=request.POST['id']).get()
            Connection_Data.objects.create(connection=connection, data=data).save()
            return redirect('./')
        return redirect('./')

@csrf_exempt
def connection_data_del(request, connection_id, data_id):
    if request.method == 'GET':
        data=Data.objects.filter(id=data_id).get()
        context={'element': data}
        return render(request, 'capabilitydatadel.html', context)
    if request.method == 'DELETE':
        connection = Connection.objects.filter(id=connection_id).get()
        data = Data.objects.filter(id=data_id).get()
        Connection_Data.objects.filter(connection=connection, data=data).delete()
        return redirect('../')