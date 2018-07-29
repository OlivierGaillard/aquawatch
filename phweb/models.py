from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Deg(models.Model):
    celsius = models.DecimalField(decimal_places=3, max_digits=5)
    date    = models.DateTimeField(default=timezone.now)
    user    = models.ForeignKey(User, null=True)
    def __str__(self):
        return repr(self.celsius) + '/' +  repr(self.date)

    def get_value(self):
        return self.celsius

    def get_graph_name():
        return "Température"

class Ph(models.Model):
    phval = models.DecimalField(decimal_places=3, max_digits=5)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return repr(self.phval) + '/' + repr(self.date)

    def get_value(self):
        return self.phval

    def get_graph_name():
        return "pH"

class Redox(models.Model):
    redoxval = models.DecimalField(decimal_places=1, max_digits=4)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return repr(self.redoxval) + '/' + repr(self.date)

    def get_value(self):
        return self.redoxval

    def get_graph_name():
        return "Redox"

class Piscine(models.Model):
    user = models.ForeignKey(User, null=True)
    capacity = models.IntegerField(verbose_name="Capacité en litres")
    enable_shutdown = models.BooleanField(default=False)
    enable_reading  = models.BooleanField(default=False)
    do_update = models.BooleanField(default=False)
    hours_of_readings = models.CharField(max_length=50, default='8,13,19')
    log_level = models.CharField(max_length=50, default='DEBUG')

class PiscineLog(models.Model):
    user = models.ForeignKey(User, null=True)
    log = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class Battery(models.Model):
    user = models.ForeignKey(User, null=True)
    date = models.DateTimeField(default=timezone.now)
    battery_charge = models.IntegerField(verbose_name="Charge in percent", default=1)




