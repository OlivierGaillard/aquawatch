from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

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

