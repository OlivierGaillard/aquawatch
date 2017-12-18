from django.db import models
from django.utils import timezone

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Water(models.Model):
    date = models.DateTimeField(default=timezone.now)
    available = models.BooleanField()
    city = models.ForeignKey(City)
    district = models.ForeignKey(District)



