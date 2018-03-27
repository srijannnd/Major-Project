from django.db import models
from authentication.models import User
# Create your models here.


class Issues(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, max_length=200)
    description = models.TextField(default="")


class BodyLocations(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, max_length=200)


class BodySubLocations(models.Model):
    bodyLocation = models.ForeignKey(BodyLocations, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, max_length=200)


class Symptoms(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, max_length=200)
    bodySubLocation = models.TextField(default="")
    selector_status = models.TextField(default="")


class SymptomRelatedIssue(models.Model):
    symptom = models.ForeignKey(Symptoms, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200)
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE)
    ranking = models.SmallIntegerField(default=0)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200)
    age = models.SmallIntegerField(blank=True)
    symptoms = models.TextField(blank=True)
    issues = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
