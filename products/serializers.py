from django.forms import widgets
from rest_framework import serializers
from models import *


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = tuple(f.name for f in Car._meta.fields)


class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = tuple(f.name for f in Furniture._meta.fields)


class AudiobookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audiobook
        fields = tuple(f.name for f in Audiobook._meta.fields)


class HologramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hologram
        fields = tuple(f.name for f in Hologram._meta.fields)