import uuid

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from device.models import Device
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