# Generated by Django 2.0.2 on 2018-03-27 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vdoc', '0017_auto_20180327_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='issues_list',
            new_name='issues',
        ),
        migrations.RenameField(
            model_name='report',
            old_name='symptoms_list',
            new_name='symptoms',
        ),
    ]
