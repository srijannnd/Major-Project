from authentication.utils import login_check
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from authentication.models import *
from vdoc.helpers.diagnosis import diagnosis_helper
from vdoc.helpers import PriaidDiagnosisClient
from vdoc.helpers.config import *
from vdoc.helpers.save_data import save_data_helper, save_symptom_issue_mapping_helper
from vdoc.helpers.dictionary import selector_status_dict, gender_dict
from vdoc.helpers.reportsList import reports_list_helper, common_symptoms_and_issues_helper
from vdoc.models import *


# Create your views here.


@api_view(['POST'])
def symptom_list(request):
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
@api_view(['POST'])
def save_data(request):
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


@api_view(['POST'])
def issue_list(request):
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


@api_view(['POST'])
def body_location_list(request):
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


@api_view(['POST'])
def body_sub_location_list(request):
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


@api_view(['POST'])
def issue_info(request):
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


@api_view(['POST'])
def diagnosis(request):
    data = request.data
    try:
        flag, user_id = login_check(data['token'], request.get_host())
        if flag:
            response, issues = diagnosis_helper(data['gender'], data['age'], data['symptoms'])
            if len(issues) > 0:
                Report.objects.create(user=User.objects.get(pk=user_id), gender=data['gender'],
                                      age=data['age'], symptoms='#'.join(map(str, data['symptoms'])),
                                      issues='#'.join(map(str, issues)))
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def body_location_related_symptoms(request):
    data = request.data
    try:
        flag, user_id = login_check(data['token'], request.get_host())
        if flag:
            response = []
            for symptom in Symptoms.objects.all():
                if data['selector_status'] in symptom.selector_status.split("#") \
                        and data['body_sub_location_id'] in map(int, symptom.bodySubLocation.split("#")):
                    response.append({"ID": symptom.id,
                                     "Name": symptom.name})
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def save_symptom_issue_mapping(request):
    data = request.data
    try:
        flag, user_id = login_check(data['token'], request.get_host())
        if flag:
            result = save_symptom_issue_mapping_helper()
            response = dict()
            response['status'] = 'data not updated' if result is False else 'data updated successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def reports_list(request):
    data = request.data
    try:
        flag, user_id = login_check(data['token'], request.get_host())
        if flag:
            response = reports_list_helper(user_id)
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def common_symptoms_and_issues(request):
    data = request.data
    try:
        flag, user_id = login_check(data['token'], request.get_host())
        if flag:
            most_common_symptoms, most_common_issues = common_symptoms_and_issues_helper()
            response = {
                'most_common_symptoms': most_common_symptoms,
                'most_common_issues': most_common_issues
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'user': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
