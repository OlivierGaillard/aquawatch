from rest_framework import serializers
from .models import Deg, Ph, Redox, Piscine, Battery

class DegreeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Deg
        fields = ('id', 'celsius', 'date', 'user')

class PhSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Ph
        fields = ('id', 'phval', 'date', 'user')

class RedoxSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Redox
        fields = ('id', 'redoxval', 'date', 'user')

class PiscineSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Piscine
        fields = ('user', 'enable_shutdown', 'do_update', 'time_beetween_readings')


class BatterySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Battery
        fields = ('user', 'battery_charge')

