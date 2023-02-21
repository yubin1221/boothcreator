import uuid

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from data.models import Data


# Create your views here.


# Create your views here.
@csrf_exempt
def dataList(request):
    if request.method == 'GET':
        data_list = Data.objects.all()
        context = {'list': data_list, 'category': 'data'}
        return render(request, 'list3.html', context)
    if request.method == 'POST':
        checkbox_array=request.POST.getlist('array[]')
        Data.objects.create(id=uuid.uuid4(), name=request.POST['name'], 
                            primitive=request.POST['primitive'],
                            label_ko=request.POST['label_ko'],
                            label_en=request.POST['label_en'],
                            default_value=request.POST['default_value'],
                            unit_of_value=request.POST['unit_of_value'],
                            min_length=request.POST['min_length'],
                            max_length=request.POST['max_length'],
                            format=request.POST['format'],
                            minimum=request.POST['minimum'],
                            maximum=request.POST['maximum'],
                            pattern=request.POST['pattern'],
                            multiple_of=request.POST['multiple_of'],
                            is_category= "category" in checkbox_array,
                            has_length_limit="length" in checkbox_array,
                            has_range_limit="range" in checkbox_array
                            ).save()
        data_list = Data.objects.all()
        context = {'list': data_list, 'category': 'data'}
        return render(request, 'list3.html', context)

@csrf_exempt
def dataInfo(request, data_id):
    if request.method == 'GET':
        data = Data.objects.filter(id=data_id)
        data = data.get()
        context = {'category': 'data', 'sub_category': 'data', 'element': data}
        return render(request, 'dataviewer.html', context)

    if request.method == 'POST':
        data = Data.objects.filter(id=data_id)
        data = data.get()
        if request.POST['name'] == '':
            new_name = data.name
        else:
            new_name = request.POST['name']
        if request.POST['primitive'] == '':
            new_primitive = data.primitive
        else:
            new_primitive = request.POST['primitive']
        if request.POST['label_ko'] == '':
            new_label_ko = data.label_ko
        else:
            new_label_ko = request.POST['label_ko']
        if request.POST['label_en'] == '':
            new_label_en = data.label_en
        else:
            new_label_en = request.POST['label_en']
        if request.POST['default_value'] == '':
            new_default_value = data.default_value
        else:
            new_default_value = request.POST['default_value']
        if request.POST['unit_of_value'] == '':
            new_unit_of_value = data.unit_of_value
        else:
            new_unit_of_value = request.POST['unit_of_value']
        if request.POST['min_length'] == '':
            new_min_length = data.min_length
        else:
            new_min_length = request.POST['min_length']
        if request.POST['max_length'] == '':
            new_max_length = data.max_length
        else:
            new_max_length = request.POST['max_length']
        if request.POST['format'] == '':
            new_format = data.format
        else:
            new_format = request.POST['format']
        if request.POST['minimum'] == '':
            new_minimum = data.minimum
        else:
            new_minimum = request.POST['minimum']
        if request.POST['maximum'] == '':
            new_maximum = data.maximum
        else:
            new_maximum = request.POST['maximum']
        if request.POST['pattern'] == '':
            new_pattern = data.pattern
        else:
            new_pattern = request.POST['pattern']
        if request.POST['multiple_of'] == '':
            new_multiple_of = data.multiple_of
        else:
            new_multiple_of = request.POST['multiple_of']

        checkbox_array=request.POST.getlist('array[]')
        Data.objects.filter(id=data_id).update(
            name=new_name,
            primitive=new_primitive,
            label_ko=new_label_ko,
            label_en=new_label_en,
            default_value=new_default_value,
            unit_of_value=new_unit_of_value,
            min_length=new_min_length,
            max_length=new_max_length,
            format=new_format,
            minimum=new_minimum,
            maximum=new_maximum,
            pattern=new_pattern,
            multiple_of=new_multiple_of,
            is_category="category" in checkbox_array,
            has_length_limit="length" in checkbox_array,
            has_range_limit="range" in checkbox_array)
        data = Data.objects.filter(id=data_id)
        data = data.get()
        context = {'category': 'data', 'sub_category': 'data', 'element': data}
        return render(request, 'dataviewer.html', context)
    if request.method == 'DELETE':
        Data.objects.filter(id=data_id).delete()
        return redirect('../')

