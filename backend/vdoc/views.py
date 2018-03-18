from authentication.utils import login_check
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from authentication.models import *
from vdoc.helpers.diagnosis import diagnosis
from vdoc.helpers import PriaidDiagnosisClient
from vdoc.helpers.config import *
from vdoc.models import *
from vdoc.helpers.save_data import save_data_helper
from vdoc.serializers import *
# Create your views here.


class SymptomChecker(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                result = diagnosis(data)
                print(result)
                return Response({'flag': flag, 'id': user_id}, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SymptomList(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                symptoms = Symptoms.objects.all()
                serializer = SymptomSerializer(symptoms, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# api to save list of symptoms, body locations and issues in the database
class SaveData(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                save_status = save_data_helper()
                return Response({'flag': flag, 'id': user_id, 'status': save_status}, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IssueList(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                issues = Issues.objects.all()
                serializer = IssueSerializer(issues, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BodyLocationList(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                body_locations = BodyLocations.objects.all()
                serializer = BodyLocationSerializer(body_locations, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BodySubLocationList(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                body_sub_locations = BodySubLocations.objects.filter(bodyLocation=data['body_location_id'])
                serializer = BodySubLocationSerializer(body_sub_locations, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)