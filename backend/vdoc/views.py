from authentication.utils import login_check
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from authentication.models import *
from vdoc.helpers.diagnosis import diagnosis
from vdoc.helpers import PriaidDiagnosisClient
from vdoc.helpers.config import *
from vdoc.helpers.save_data import save_data_helper, save_symptom_issue_mapping
from vdoc.helpers.dictionary import selector_status_dict, gender_dict
from vdoc.models import *
# Create your views here.


class SymptomList(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                if data['gender'] == 'male':
                    symptoms = Symptoms.objects.filter(selector_status__startswith='man').values('id',
                                                                                                 'name')
                else:
                    symptoms = Symptoms.objects.all().values('id',
                                                             'name')
                return Response(symptoms, status=status.HTTP_200_OK)
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
                issues = Issues.objects.all().values('id', 'name')
                return Response(issues, status=status.HTTP_200_OK)
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
                body_locations = BodyLocations.objects.all().values('id', 'name')
                return Response(body_locations, status=status.HTTP_200_OK)
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
                body_sub_locations = BodySubLocations.objects.filter(
                    bodyLocation=data['body_location_id']
                ).values('id', 'name')
                return Response(body_sub_locations, status=status.HTTP_200_OK)
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
                response = diagnosis(data['gender'], data['age'], data['symptoms'])
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


class SaveSymptomIssueMapping(APIView):

    def post(self, request):
        data = request.data
        try:
            flag, user_id = login_check(data['token'], request.get_host())
            if flag:
                result = save_symptom_issue_mapping()
                response = dict()
                response['status'] = 'data not updated' if result is False else 'data updated successfully'
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
