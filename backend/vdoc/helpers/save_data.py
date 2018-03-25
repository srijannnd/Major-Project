from vdoc.helpers import PriaidDiagnosisClient
from vdoc.helpers.config import *
from vdoc.models import *
from vdoc.helpers.dictionary import selector_status_dict, gender_dict
import requests


def save_data_helper():
    obj = PriaidDiagnosisClient.DiagnosisClient(username, password, authUrl, language, healthUrl)
    symptom_list = obj.loadSymptoms()
    body_location_list = obj.loadBodyLocations()
    issue_list = obj.loadIssues()
    symptom_list_status = "Symptom List Not Updated"
    body_location_list_status = "Body Location List Not Updated"
    issue_list_status = "Issue List Not Updated"
    body_sub_location_list_status = "Body Sub Location List Not Updated"
    body_location_in_symptoms = "Body Sub Locations in Symptoms Not Updated"

    # Save all Symptoms
    try:
        for symptom in symptom_list:
            Symptoms.objects.create(id=symptom['ID'], name=symptom['Name'])
        symptom_list_status = "Symptom List Updated Successfully"
    except Exception as e:
        print(e)

    # Save all Issues
    try:
        for issue in issue_list:
            Issues.objects.create(id=issue['ID'], name=issue['Name'])
        issue_list_status = "Issue List Updated Successfully"
    except Exception as e:
        print(e)

    # Save all Body Locations
    try:
        for location in body_location_list:
            BodyLocations.objects.create(id=location['ID'], name=location['Name'])
        body_location_list_status = "Body Location List Updated Successfully"
    except Exception as e:
        print(e)

    # Save all Body Sub Locations
    try:
        list = BodyLocations.objects.all()
        for body_location in list:
            body_sublocation_list = obj.loadBodySubLocations(body_location.id)
            for sub_location in body_sublocation_list:
                BodySubLocations.objects.create(
                    bodyLocation=body_location,
                    id=sub_location['ID'],
                    name=sub_location['Name'])
        body_sub_location_list_status = "Body Sub Location List Updated Successfully"
    except Exception as e:
        print(e)

    # Save Issue Info
    try:
        for issue in Issues.objects.all():
            if issue.description == "":
                issue.description = obj.loadIssueInfo(issue.id)
                issue.save()
    except Exception as e:
        print(e)
    # Save Body Locations in Symptoms
    try:
        sub_locations = BodySubLocations.objects.all()
        for sub_location in sub_locations:
            for key, value in selector_status_dict.items():
                symptoms = obj.loadSublocationSymptoms(sub_location.id, value)
                for symptom in symptoms:
                    query_obj = Symptoms.objects.get(id=int(symptom['ID']))
                    symptom_locations_list = [] if query_obj.bodySubLocation == "" else \
                        query_obj.bodySubLocation.split('#')
                    symptom_selector_status_list = [] if query_obj.selector_status == "" else\
                        query_obj.selector_status.split('#')
                    if str(sub_location.id) not in symptom_locations_list:
                        symptom_locations_list.append(sub_location.id)
                        query_obj.bodySubLocation = "#".join(map(str, symptom_locations_list))
                    if key not in symptom_selector_status_list:
                        symptom_selector_status_list.append(key)
                        query_obj.selector_status = "#".join(symptom_selector_status_list)
                    query_obj.save()
        body_location_in_symptoms = "Body Sub Locations in Symptoms Updated Successfully"
    except Exception as e:
        print(e)

    return {'symptom_list_status': symptom_list_status,
            'body_location_list_status': body_location_list_status,
            'issue_list_status': issue_list_status,
            'body_sub_location_list_status': body_sub_location_list_status,
            'body_location_in_symptoms': body_location_in_symptoms}


def save_symptom_issue_mapping():
    try:
        url_symptom_list = "http://127.0.0.1:8000/api/symptomList/"
        url_diagnosis = "http://127.0.0.1:8000/api/diagnosis/"
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTI2NTc1Mzk5fQ.\
        vFOGIUShI29KvXVSmb7jl5iXIBJkizk-irGsw-V_H0M"

        json_list = {
            "token": token
        }
        list_request = requests.post(url_symptom_list, json=json_list)
        symptoms_list = [symptom['id'] for symptom in eval(list_request.content)]
        genders = ["male", "female"]
        query_set = symptoms_list
        for gender in genders:
            for symptom in query_set:
                symptom_obj = Symptoms.objects.get(id=symptom)
                json_diagnosis = {
                    "token": token,
                    "gender": gender,
                    "age": 20,
                    "symptoms": [symptom]
                }
                diagnosis_request = requests.post(url_diagnosis, json=json_diagnosis)
                issue_list = eval(diagnosis_request.content)
                # issue_id_list = []
                # for issue in issue_list:
                #     if 'ID' in issue:
                #         issue_id_list.append(issue['ID'])
                if len(issue_list) > 0:
                    for issue in issue_list:
                        issue_obj = Issues.objects.get(id=issue['ID'])
                        SymptomRelatedIssue.objects.create(
                            symptom=symptom_obj,
                            gender=gender,
                            issue=issue_obj,
                            ranking=issue['Ranking'],
                        )
        return True
    except Exception as e:
        print(e)
        return False
