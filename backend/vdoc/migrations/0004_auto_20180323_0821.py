# Generated by Django 2.0.2 on 2018-03-23 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vdoc', '0003_remove_issues_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='symptoms',
            name='bodySubLocation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vdoc.BodySubLocations'),
        ),
        migrations.AddField(
            model_name='symptoms',
            name='selector_status',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
