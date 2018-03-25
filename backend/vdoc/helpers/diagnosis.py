from vdoc.helpers import PriaidDiagnosisClient
from vdoc.helpers.config import *
from vdoc.models import *


def diagnosis(gender, age, symptoms):
    for symptom in symptoms:
        issues = SymptomRelatedIssue.objects.filter(symptom=symptom,
                                                    gender=gender)
