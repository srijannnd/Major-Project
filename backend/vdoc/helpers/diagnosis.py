from vdoc.models import *
from django.db.models import F


def diagnosis(gender, age, symptoms):
    issue_list = []
    for symptom in symptoms:
        issues = list(SymptomRelatedIssue.objects.filter(symptom=symptom,
                                                         gender=gender
                                                         ).annotate(ID=F('issue'),
                                                                    Ranking=F('ranking')
                                                                    ).values('ID', 'Ranking'))
        for issue in issues:
            issue_list.append(issue)

    issue_id_list = set([i['ID'] for i in issue_list])
    result = []
    for issue in issue_id_list:
        ranks = []
        for issue_obj in issue_list:
            if issue_obj['ID'] == issue:
                ranks.append(issue_obj['Ranking'])
        weight = 0
        for rank in ranks:
            weight += (11 - rank)/len(symptoms)
        result.append({'ID': issue, 'weight': weight})

    sorted_issues = sorted(result, key=lambda k: k['weight'], reverse=True)
    filtered_issues = list(filter(lambda x: x['weight'] > 5, sorted_issues))
    filtered_issues = filtered_issues[:5] if len(filtered_issues) > 5 else filtered_issues
    data = [{'ID': filtered_issues[i]['ID'], 'Ranking': i+1} for i in range(len(filtered_issues))]
    issues = [issue['ID'] for issue in filtered_issues]
    return data, issues
