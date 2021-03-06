# Generated by Django 2.0 on 2018-11-08 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20181106_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template_Global',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('template', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_template_global_related', to='api.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='template_worker',
            name='template_hit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='templates_used', to='api.Template_HIT'),
        ),
        migrations.AlterUniqueTogether(
            name='template_global',
            unique_together={('project', 'name')},
        ),
    ]
