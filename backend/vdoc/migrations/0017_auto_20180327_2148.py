# Generated by Django 2.0.2 on 2018-03-27 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vdoc', '0016_remove_report_issue_ranks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='issues',
            new_name='issues_list',
        ),
        migrations.RenameField(
            model_name='report',
            old_name='symptoms',
            new_name='symptoms_list',
        ),
    ]