from rest_framework import serializers
from vdoc.models import *


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptoms
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'


class BodyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyLocations
        fields = '__all__'


class BodySubLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodySubLocations
        fields = '__all__'
