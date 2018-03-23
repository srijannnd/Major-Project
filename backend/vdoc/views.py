from authentication.utils import login_check
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from authentication.models import *
from vdoc.helpers.diagnosis import diagnosis
from vdoc.helpers import PriaidDiagnosisClient
from vdoc.helpers.config import *
from vdoc.helpers.save_data import save_data_helper
from vdoc.serializers import *
from vdoc.helpers.dictionary import selector_status_dict, gender_dict
# Create your views here.


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


class IssueInfo(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                issue = Issues.objects.get(id=data['issue_id'])
                response = eval(issue.description)
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Diagnosis(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                response = []
                obj = PriaidDiagnosisClient.DiagnosisClient(username, password, authUrl, language, healthUrl)
                year = datetime.today().year - data['age']
                gender = gender_dict[data['gender']]
                issues_list = obj.loadDiagnosis(data['symptoms'], gender, year)
                for issue in issues_list:
                    response.append({"ID": issue['Issue']["ID"], 'Ranking': issue['Issue']['Ranking']})
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RelatedSymptoms(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                obj = PriaidDiagnosisClient.DiagnosisClient(username, password, authUrl, language, healthUrl)

                year = datetime.today().year - data['age']
                gender = gender_dict[data['gender']]
                response = obj.loadProposedSymptoms(data['symptoms'], gender, year)
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BodyLocationRelatedSymptoms(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                response = []
                for symptom in Symptoms.objects.all():
                    if data['selector_status'] in symptom.selector_status.split("#")\
                            and data['body_sub_location_id'] in map(int, symptom.bodySubLocation.split("#")):
                        response.append({"ID": symptom.id,
                                         "Name": symptom.name})
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
