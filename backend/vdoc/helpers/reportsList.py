from vdoc.models import Report, Symptoms, Issues


def reports_list(user_id):
    reports = Report.objects.filter(user=user_id).values()
    for report in reports:
        report['symptoms'] = Symptoms.objects.filter(
            id__in=map(int, report['symptoms'].split('#'))).values('id', 'name')
        report['issues'] = Issues.objects.filter(
            id__in=map(int, report['issues'].split('#'))).values()
        for issue in report['issues']:
            issue['description'] = eval(issue['description'])
    return reports
