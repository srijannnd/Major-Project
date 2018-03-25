from django.db import models

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
