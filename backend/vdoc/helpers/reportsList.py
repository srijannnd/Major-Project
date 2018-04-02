from vdoc.models import Report, Symptoms, Issues
from django.db.models import F
from collections import Counter


def reports_list_helper(user_id):
    reports = Report.objects.filter(user=user_id).values()
    for report in reports:
        report['symptoms'] = Symptoms.objects.filter(
            id__in=map(int, report['symptoms'].split('#'))).values('id', 'name')
        report['issues'] = Issues.objects.filter(
            id__in=map(int, report['issues'].split('#'))).annotate(info=F('description'),
                                                                   ID=F('id')).values(
            'ID', 'info'
        )
        for issue in report['issues']:
            issue['info'] = eval(issue['info'])
    return reports


def common_symptoms_and_issues_helper():
    reports = Report.objects.all().values('issues', 'symptoms')
    most_common_symptoms = most_common_symptoms_helper(reports)
    most_common_issues = most_common_issues_helper(reports)
    return most_common_symptoms, most_common_issues


def most_common_symptoms_helper(reports):
    res = list()
    symptoms_list = list()
    for report in reports:
        symptoms_list.extend(report['symptoms'].split('#'))
    common_symptoms = Counter(symptoms_list).most_common(5)
    for key, value in common_symptoms:
        res.append({
            'label': Symptoms.objects.get(id=key).name,
            'value': value
        })
    return res


def most_common_issues_helper(reports):
    res = list()
    issues_list = list()
    for report in reports:
        issues_list.extend(report['issues'].split('#'))
    common_issues = Counter(issues_list).most_common(5)
    for key, value in common_issues:
        res.append({
            'label': Issues.objects.get(id=key).name,
            'value': value
        })
    return res
