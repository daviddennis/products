from django.core import serializers
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from models import *
from serializers import *
import json
from django.db import connection
#from django.db.models.signals import class_prepared


@csrf_exempt
def cars(request, pk=None):
    return generic_rest_view(request, Car, CarSerializer, pk=pk)



# def cars_add(request):
#     field_name = "dog"
#     #Car.objects.raw('ALTER TABLE products_car ADD %s %schar(500)' % (field_name, "var"))
#     #return generic_rest_view(request, Car, CarSerializer)
#     cursor = connection.cursor()
#     cursor.execute('ALTER TABLE products_car ADD %s %schar(500)' % (field_name, "var"))
#     return generic_rest_view(request, Car, CarSerializer)

# def add_field(sender, **kwargs):
#     from django.db.models import CharField
#     field = CharField("NewField", max_length=100, null=True, blank=True)
#     field.contribute_to_class(Car, "new_field")

# class_prepared.connect(add_field)

@csrf_exempt
def furniture(request, pk=None):
    return generic_rest_view(request, Furniture, FurnitureSerializer, pk=pk)


@csrf_exempt
def audiobooks(request, pk=None):
    return generic_rest_view(request, Audiobook, AudiobookSerializer, pk=pk)


@csrf_exempt
def holograms(request, pk=None):
    return generic_rest_view(request, Hologram, HologramSerializer, pk=pk)


def generic_rest_view(request, model, model_serializer, pk=None):
    if pk:
        try:
            model_instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            # Read
            serializer = model_serializer(model_instance)
            return JSONResponse(serializer.data)

        elif request.method == 'PUT':
            # Update
            data = JSONParser().parse(request)
            serializer = model_serializer(model_instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            else:
                return JSONResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            model_instance.delete()
            return HttpResponse(status=204)
    else:
        if request.method == 'GET':
            if len(request.GET) > 0:
                # Search
                field_dict = {}
                for field in model._meta.fields:
                    if field.name in request.GET:
                        field_dict[field.name+"__icontains"] = request.GET[field.name]
                if field_dict:
                    models = model.objects.filter( **field_dict )
                else:
                    models = []
            else:
                # List
                models = model.objects.all()
            serializer = model_serializer(models, many=True)
            return JSONResponse(serializer.data)
        elif request.method == 'POST':
            # Create
            data = JSONParser().parse(request)
            serializer = model_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            else:
                return JSONResponse(serializer.errors, status=400)


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
