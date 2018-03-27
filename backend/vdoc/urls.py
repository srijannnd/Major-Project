from django.urls import path
from vdoc.views import *

app_name = "vdoc"

urlpatterns = [
    path(r'symptomList/', SymptomList.as_view()),
    path(r'issueList/', IssueList.as_view()),
    path(r'bodyLocationList/', BodyLocationList.as_view()),
    path(r'bodySubLocationList/', BodySubLocationList.as_view()),
    path(r'saveData/', SaveData.as_view()),
    path(r'issueInfo/', IssueInfo.as_view()),
    path(r'diagnosis/', Diagnosis.as_view()),
    path(r'relatedSymptoms/', RelatedSymptoms.as_view()),
    path(r'bodyLocationRelatedSymptoms/', BodyLocationRelatedSymptoms.as_view()),
    path(r'saveSymptomIssueMapping/', SaveSymptomIssueMapping.as_view()),
    path(r'reportsList/', ReportsList.as_view()),
]
