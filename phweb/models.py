from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator



class Deg(models.Model):
    celsius = models.DecimalField(decimal_places=3, max_digits=5, validators=[MinValueValidator(2)])
    date    = models.DateTimeField(default=timezone.now)
    user    = models.ForeignKey(User, null=True)
    def __str__(self):
        return repr(self.celsius) + '/' +  repr(self.date)

    def get_value(self):
        return self.celsius

    def get_graph_name():
        return "Température"

    class Meta:
        ordering = ['-date']

class Ph(models.Model):
    phval = models.DecimalField(decimal_places=3, max_digits=5, validators=[MinValueValidator(3, message="Trop acide pour être réel")])
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return repr(self.phval) + '/' + repr(self.date)

    def get_value(self):
        return self.phval

    def get_graph_name():
        return "pH"

    class Meta:
        ordering = ['-date']

class Redox(models.Model):
    redoxval = models.DecimalField(decimal_places=1, max_digits=5, validators=[MinValueValidator(50),
                                                                               MaxValueValidator(1111)])
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return repr(self.redoxval) + '/' + repr(self.date)

    def get_value(self):
        return self.redoxval

    def get_graph_name():
        return "Redox"

    class Meta:
        ordering = ['-date']

class Piscine(models.Model):
    user = models.ForeignKey(User, null=True)
    capacity = models.IntegerField(verbose_name="Capacité en litres")
    enable_shutdown = models.BooleanField(default=False)
    bigshutdown = models.BooleanField(default=False, help_text="Alarms disabled, power off")
    enable_reading  = models.BooleanField(default=False)
    do_update = models.BooleanField(default=False)
    hours_of_readings = models.CharField(max_length=50, default='8,13,19')
    log_level = models.CharField(max_length=50, default='DEBUG')

class PiscineLog(models.Model):
    user = models.ForeignKey(User, null=True)
    log = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']


class Battery(models.Model):
    user = models.ForeignKey(User, null=True)
    date = models.DateTimeField(default=timezone.now)
    battery_charge = models.IntegerField(verbose_name="Charge in percent", default=1)

    class Meta:
        ordering = ['-date']




