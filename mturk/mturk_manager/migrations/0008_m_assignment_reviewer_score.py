# Generated by Django 2.0 on 2018-03-11 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mturk_manager', '0007_auto_20180226_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='m_assignment',
            name='reviewer_score',
            field=models.FloatField(null=True),
        ),
    ]