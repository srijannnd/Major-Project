from vdoc.models import Report, Symptoms, Issues
from django.db.models import F

def reports_list(user_id):
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
