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

model_dict = {
    "cars": Car,
    "furniture": Furniture,
    "holograms": Hologram,
    "audiobooks": Audiobook
    }


@csrf_exempt
def cars(request, pk=None):
    return generic_rest_view(request, Car, CarSerializer, pk=pk)


@csrf_exempt
def furniture(request, pk=None):
    return generic_rest_view(request, Furniture, FurnitureSerializer, pk=pk)


@csrf_exempt
def audiobooks(request, pk=None):
    return generic_rest_view(request, Audiobook, AudiobookSerializer, pk=pk)


@csrf_exempt
def holograms(request, pk=None):
    return generic_rest_view(request, Hologram, HologramSerializer, pk=pk)


@csrf_exempt
def add_attribute(request, field_name):

    model = model_dict[request.path.split('/')[1].lower()]

    resp = {
            "action": "Add Attribute",
            "model": model.__name__,
            "field_name": field_name
        }

    try:
        Attribute.objects.get(
            model_type=model.__name__,
            name=field_name)
        resp['status'] = "Failure"
        resp['error_msg'] = "%s already has an attribute named '%s'" % (model.__name__, field_name)
    except Attribute.DoesNotExist:
        attribute = Attribute(
            model_type=model.__name__,
            name=field_name)
        attribute.save()
        resp['status'] = "Success"

    return JSONResponse(resp)

@csrf_exempt
def remove_attribute(request, field_name):

    model = model_dict[request.path.split('/')[1].lower()]

    resp = {
            "action": "Remove Attribute",
            "model": model.__name__,
            "field_name": field_name
        }

    try:
        attribute = Attribute.objects.get(
            model_type=model.__name__,
            name=field_name)
        attribute.delete()
        resp['status'] = "Success"
    except Attribute.DoesNotExist:
        resp['status'] = "Failure"
        resp['error_msg'] = "%s has no attribute named '%s'" % (model.__name__, field_name)

    return JSONResponse(resp)


def generic_rest_view(request, model, model_serializer, pk=None):
    if pk:
        try:
            model_instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            # Read
            serializer = model_serializer(model_instance)
            append_attributes(model, model_instance, serializer.data)
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
            attribute_field_dict = {}
            if len(request.GET) > 0:
                # Search
                field_dict = {}                
                for field in model._meta.fields:
                    if field.name in request.GET:
                        field_dict[field.name+"__icontains"] = request.GET[field.name]
                    else:
                        attribute_field_dict[field.name] = request.GET[field.name]
                if field_dict:
                    models = model.objects.filter( **field_dict )
                else:
                    models = []
            else:
                # List
                models = model.objects.all()
            # if attribute_field_dict:
            #     AttributeInstance.objects.all().\
            #         filter(attribute__model_type=model.__name__,
            #             )
            serializer = model_serializer(models, many=True)
            print serializer.data
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


def append_attributes(model, model_instance, data):
    attributes = Attribute.objects.all().filter(model_type=model.__name__)
    for attribute in attributes:
        attribute_instances = attribute.attributeinstance_set.all().\
            filter(model_id = model_instance.id)
        for attribute_instance in attribute_instances:
            data[attribute.name] = attribute_instance.value


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
