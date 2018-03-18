from django.urls import path
from vdoc.views import *

app_name = "vdoc"

urlpatterns = [
    path(r'diagnosis/', SymptomChecker.as_view()),
    path(r'symptomList/', SymptomList.as_view()),
    path(r'issueList/', IssueList.as_view()),
    path(r'bodyLocationList/', BodyLocationList.as_view()),
    path(r'bodySubLocationList/', BodySubLocationList.as_view()),
    path(r'saveData/', SaveData.as_view()),
]
