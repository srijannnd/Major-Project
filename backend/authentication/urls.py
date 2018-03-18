from django.urls import path
from authentication.views import *

app_name = "authentication"

urlpatterns = [
    path(r'users/', RegistrationAPIView.as_view()),
    path(r'users/login/', LoginAPIView.as_view()),
    path(r'user/', UserFlag.as_view()),
]
