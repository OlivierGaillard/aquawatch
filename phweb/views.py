from django.views.decorators.csrf import csrf_exempt
from .models import Deg, Ph, Redox, Piscine, Battery
from .serializers import DegreeSerializer, PhSerializer, RedoxSerializer, PiscineSerializer, BatterySerializer
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse


class DegreeViewSet(viewsets.ModelViewSet):


    serializer_class = DegreeSerializer
    #queryset = Deg.objects.all().order_by('-date')

    def get_queryset(self):
        user = self.request.user
        return Deg.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['POST'])
    def update_deg(self, request, pk):
        """Update a measure. Will never be used but who knows?"""
        deg = self.get_object()
        serializer = DegreeSerializer(data=request.data)
        if serializer.is_valid():
            deg.celsius = serializer.data['celsius']
            deg.save()
            return HttpResponse({'status' : 'degree updated'})
        else:
            return HttpResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    def last(self, request, pk=None):
        """Get the last value."""
        user = self.request.user
        deg = Deg.objects.filter(user=self.request.user).last()
        serializer = DegreeSerializer(deg)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def delete(self, request, pk):
        deg = self.get_object()
        deg.delete()
        return HttpResponse({'status' : 'degree deleted'})

class PhViewSet(viewsets.ModelViewSet):

    serializer_class = PhSerializer

    def get_queryset(self):
        user = self.request.user
        return Ph.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['POST'])
    def update_ph(self, request, pk):
        """Update a measure. Will never be used but who knows?"""
        ph = self.get_object()
        serializer = PhSerializer(data=request.data)
        if serializer.is_valid():
            ph.phval = serializer.data['phval']
            ph.save()
            return HttpResponse({'status': 'pH updated'})
        else:
            return HttpResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def delete(self, request, pk):
        ph = self.get_object()
        ph.delete()
        return HttpResponse({'status': 'ph deleted'})

class RedoxViewSet(viewsets.ModelViewSet):

    serializer_class = RedoxSerializer

    def get_queryset(self):
        user = self.request.user
        return Redox.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['POST'])
    def update_redox(self, request, pk):
        """Update a measure. Will never be used but who knows?"""
        redox = self.get_object()
        serializer = RedoxSerializer(data=request.data)
        if serializer.is_valid():
            redox.redoxval = serializer.data['redoxval']
            redox.save()
            return HttpResponse({'status': 'redox updated'})
        else:
            return HttpResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def delete(self, request, pk):
        redox = self.get_object()
        redox.delete()
        return HttpResponse({'status': 'redox deleted'})


class PiscineViewSet(viewsets.ModelViewSet):

    serializer_class = PiscineSerializer

    def get_queryset(self):
        user = self.request.user
        return Piscine.objects.filter(user=user)


class BatteryViewSet(viewsets.ModelViewSet):
    serializer_class = BatterySerializer

    def get_queryset(self):
        user = self.request.user
        return Battery.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['POST'])
    def update_charge(self, request, pk):
        """Update battery charge. Will never be used but who knows?"""
        battery = self.get_object()
        serializer = BatterySerializer(data=request.data)
        if serializer.is_valid():
            battery.battery_charge = serializer.data['battery_charge']
            battery.save()
            return HttpResponse({'status': 'battery charge updated'})
        else:
            return HttpResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
