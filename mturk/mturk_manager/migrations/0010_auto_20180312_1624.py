# Generated by Django 2.0 on 2018-03-12 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mturk_manager', '0009_auto_20180311_2019'),
    ]

    operations = [
        migrations.CreateModel(
            name='m_Template_Global',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('template', models.TextField()),
                ('fk_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templates_global', to='mturk_manager.m_Project')),
            ],
        ),
        migrations.AddField(
            model_name='m_project',
            name='fk_template_global_main',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project', to='mturk_manager.m_Template_Global'),
        ),
        migrations.AlterUniqueTogether(
            name='m_template_global',
            unique_together={('name', 'fk_project')},
        ),
    ]
