# Generated by Django 2.0.2 on 2018-03-23 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vdoc', '0009_auto_20180323_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='issues',
            name='description',
            field=models.TextField(default=''),
        ),
    ]