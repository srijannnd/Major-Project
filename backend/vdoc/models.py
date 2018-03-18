from django.db import models

# Create your models here.


class Symptoms(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, max_length=200)


class Issues(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True)
    name = models.CharField(blank=True, max_length=200)


class BodyLocations(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, max_length=200)


class BodySubLocations(models.Model):
    bodyLocation = models.ForeignKey(BodyLocations, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, max_length=200)
