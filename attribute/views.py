import uuid

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from attribute.models import Attribute


# Create your views here.
@csrf_exempt
def attributeList(request):
    if request.method == 'GET':
        attribute_list = Attribute.objects.all()
        context = {'list': attribute_list, 'category': 'attribute'}
        return render(request, 'list.html', context)
    if request.method == 'POST':
        Attribute.objects.create(id=uuid.uuid4(), name=request.POST['name'], version=request.POST['version'],
                              vendor=request.POST['vendor']).save()
        attribute_list = Attribute.objects.all()
        context = {'list': attribute_list, 'category': 'attribute'}
        return render(request, 'list.html', context)