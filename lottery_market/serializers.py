from rest_framework import serializers

from .models import *


class OddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odd
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    update = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    t = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    odd = OddSerializer()

    class Meta:
        model = Market
        fields = '__all__'
