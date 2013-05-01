from django.core import serializers
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from models import *
from serializers import *
import json
from django.db import connection


model_dict = {
    "cars": Car,
    "furniture": Furniture,
    "holograms": Hologram,
    "audiobooks": Audiobook
    }

@csrf_exempt
def show_products(request):
    return JSONResponse({
            'cars': 'http://173.255.235.144/cars',
            'furniture': 'http://173.255.235.144/furniture',
            'holograms': 'http://173.255.235.144/holograms',
            'audiobooks': 'http://173.255.235.144/audiobooks',
        })

@csrf_exempt
def cars(request, pk=None):
    return generic_rest_view(request, Car, CarSerializer, CarAttribute, pk=pk)


@csrf_exempt
def furniture(request, pk=None):
    return generic_rest_view(request, Furniture, FurnitureSerializer, FurnitureAttribute, pk=pk)


@csrf_exempt
def audiobooks(request, pk=None):
    return generic_rest_view(request, Audiobook, AudiobookSerializer, AudiobookAttribute, pk=pk)


@csrf_exempt
def holograms(request, pk=None):
    return generic_rest_view(request, Hologram, HologramSerializer, HologramAttribute, pk=pk)


@csrf_exempt
def add_attribute(request, field_name):

    model = model_dict[request.path.split('/')[1].lower()]

    resp = {
            "action": "Add Attribute",
            "model": model.__name__,
            "field_name": field_name
        }

    if Attribute.objects.all().filter(
        model_type=model.__name__,
        name=field_name):
        resp['status'] = "Failure"
        resp['error_msg'] = "%s already has an attribute named '%s'" % (model.__name__, field_name)
    else:
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


def generic_rest_view(request, model, model_serializer, attribute_model, pk=None):
    if pk:
        try:
            model_instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            # Read
            serializer = model_serializer(model_instance)
            append_attributes_to_model(model, model_instance, attribute_model, serializer.data)
            return JSONResponse(serializer.data)

        elif request.method == 'PUT':
            # Update
            put_params = json.loads(request.body)
            save_attributes_from_params(model, model_instance, put_params, attribute_model)
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
                field_names = [f.name for f in model._meta.fields] + ['id']
                for field_name in request.GET:
                    if field_name in field_names:
                        field_dict[field_name+"__icontains"] = request.GET[field_name]
                    else:
                        attribute_field_dict[field_name] = request.GET.get(field_name)
                if field_dict:
                    models = model.objects.filter( **field_dict )
                else:
                    if request.GET:
                        models = model.objects.all()
                    else:
                        models = []
            else:
                # List
                models = model.objects.all()
            serializer = model_serializer(models, many=True)
            for model_i, data in zip(models, serializer.data):
                append_attributes_to_model(model, model_i, attribute_model, data)
            data = serializer.data
            for attr_name, attr_value in attribute_field_dict.items():
                data = [d for d in data if d.get(attr_name) == attr_value]
            return JSONResponse(data)

        elif request.method == 'POST':
            # Create
            data = JSONParser().parse(request)
            serializer = model_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                model_instance = model.objects.get(pk=serializer.data.get('id'))
                post_params = request.POST
                save_attributes_from_params(model, model_instance, post_params, attribute_model)
                return JSONResponse(serializer.data, status=201)
            else:
                return JSONResponse(serializer.errors, status=400)


def append_attributes_to_model(model, model_instance, attribute_model, data):
    for attribute in Attribute.objects.all().filter(model_type=model.__name__):
        attribute_filters = {
            "attribute__model_type": model.__name__,
            "attribute__name": attribute.name,
            "%s__pk" % model.__name__.lower(): model_instance.id
        }
        attribute_instances = attribute_model.objects.all().filter( **attribute_filters )
        for attribute_instance in attribute_instances:
            data[attribute.name] = attribute_instance.value


def save_attributes_from_params(model, model_instance, params, attribute_model):
    attributes = Attribute.objects.all().filter(model_type=model.__name__)
    for field_name in params:
        for attribute in attributes:
            if field_name == attribute.name:
                attr_instance_data = {
                    model.__name__.lower(): model_instance,
                    "attribute": attribute,
                    "value": params[field_name]
                }
                attr_instance = attribute_model( **attr_instance_data )
                attr_instance.save()


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
