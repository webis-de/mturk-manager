# Generated by Django 2.2.1 on 2019-07-13 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_auto_20190710_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celerytasks',
            name='status',
            field=models.IntegerField(choices=[(0, 'CREATED'), (1, 'PROGRESS'), (2, 'FINISHED')]),
        ),
    ]
