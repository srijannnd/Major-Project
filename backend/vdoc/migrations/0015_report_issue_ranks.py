# Generated by Django 2.0.2 on 2018-03-27 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vdoc', '0014_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='issue_ranks',
            field=models.TextField(blank=True),
        ),
    ]