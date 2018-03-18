from vdoc.helpers import PriaidDiagnosisClient
from vdoc.helpers.config import *
from vdoc.models import *


def save_data_helper():
    obj = PriaidDiagnosisClient.DiagnosisClient(username, password, authUrl, language, healthUrl)
    symptom_list = obj.loadSymptoms()
    body_location_list = obj.loadBodyLocations()
    issue_list = obj.loadIssues()
    symptom_list_status = "Symptom List Not Updated"
    body_location_list_status = "Body Location List Not Updated"
    issue_list_status = "Issue List Not Updated"
    body_sub_location_list_status = "Body Sub Location List Not Updated"

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
        body_location_list_status = "Body Location List Updated Successfully"
    except Exception as e:
        print(e)

    # Save all Body Locations
    try:
        for location in body_location_list:
            BodyLocations.objects.create(id=location['ID'], name=location['Name'])
        issue_list_status = "Issue List Updated Successfully"
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

    return {'symptom_list_status': symptom_list_status,
            'body_location_list_status': body_location_list_status,
            'issue_list_status': issue_list_status,
            'body_sub_location_list_status': body_sub_location_list_status}
