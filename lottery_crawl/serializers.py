from rest_framework import serializers

from models import *


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point


class SampleMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleMeta
