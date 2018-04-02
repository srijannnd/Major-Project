from django.urls import path
from vdoc.views import *

app_name = "vdoc"

urlpatterns = [
    path(r'symptomList/', symptom_list),
    path(r'issueList/', issue_list),
    path(r'bodyLocationList/', body_location_list),
    path(r'bodySubLocationList/', body_sub_location_list),
    path(r'saveData/', save_data),
    path(r'issueInfo/', issue_info),
    path(r'diagnosis/', diagnosis),
    path(r'relatedSymptoms/', related_symptoms),
    path(r'bodyLocationRelatedSymptoms/', body_location_related_symptoms),
    path(r'saveSymptomIssueMapping/', save_symptom_issue_mapping),
    path(r'reportsList/', reports_list),
    path(r'commonSymptomsAndIssue/', common_symptoms_and_issues),
]
