from django.urls import path, include, re_path, register_converter
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('workers', views.ViewSet_Workers)
# router.register('projects', views.ViewSet_Projects)

class NegativeIntConverter:
    regex = '-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value

register_converter(NegativeIntConverter, 'negint')

app_name = 'api'
urlpatterns = format_suffix_patterns([
    path('config', views.Config.as_view(), name='config'),
    path('info_projects/uniqueness/<str:name_project>', views.projects_check_uniqueness, name='projects_check_uniqueness'),
    path('projects', views.Projects.as_view(), name='projects'),
    path('projects/<str:slug_project>', views.Project.as_view(), name='project'),


    path('projects/<str:slug_project>/settings_batch', views.Settings_Batch.as_view(), name='settings_batch_for_project'),
    path('projects/<str:slug_project>/settings_batch/<int:id_settings_batch>', views.Setting_Batch.as_view(), name='setting_batch_for_project'),

    path('projects/<str:slug_project>/templates_worker', views.Templates_Worker.as_view(), name='templates_for_project'),
    path('projects/<str:slug_project>/templates_worker/<int:id_template>', views.Template_Worker.as_view(), name='template_for_project'),
    path('projects/<str:slug_project>/templates_assignment', views.Templates_Assignment.as_view(), name='templates_assignment_for_project'),
    path('projects/<str:slug_project>/templates_assignment/<int:id_template>', views.Template_Assignment.as_view(), name='template_assignment_for_project'),
    path('projects/<str:slug_project>/templates_hit', views.Templates_HIT.as_view(), name='templates_hit_for_project'),
    path('projects/<str:slug_project>/templates_hit/<int:id_template>', views.Template_HIT.as_view(), name='template_hit_for_project'),
    path('projects/<str:slug_project>/templates_global', views.Templates_Global.as_view(), name='templates_global_for_project'),
    path('projects/<str:slug_project>/templates_global/<int:id_template>', views.Template_Global.as_view(), name='template_global_for_project'),
    # path('projects/<str:slug_project>/settings_batch', views.Settings_Batch.as_view(), name='settings_batch_for_project'),

    path('projects/<str:slug_project>/count_assignments_max_per_worker', views.get_count_assignments_max_per_worker),
    path('projects/<str:slug_project>/count_assignments_max_per_worker/<negint:value>', views.set_count_assignments_max_per_worker),

    path('projects/<str:slug_project>/batches', views.Batches.as_view(), name='batches_for_project'),
    path('projects/<str:slug_project>/batches/<int:id_batch>', views.Batch.as_view(), name='batch_for_project'),
    path('projects/<str:slug_project>/batches_for_annotation', views.batches_for_annotation, name='batches_for_annotation'),
    path('projects/<str:slug_project>/download_batches', views.download_batches, name='download_batches'),
    path('projects/<str:slug_project>/download_info_batches', views.download_info_batches, name='download_info_batches'),

    path('projects/<str:slug_project>/hits', views.HITs.as_view(), name='hits_for_project'),
    path('projects/<str:slug_project>/hits_by_id', views.get_hits_by_id, name='get_by_id'),

    path('projects/<str:slug_project>/assignments', views.Assignments.as_view(), name='assignments_for_project'),
    path('projects/<str:slug_project>/assignments_by_id', views.get_assignments_by_id, name='get_by_id'),

    # path('projects/<str:slug_project>/assignments/<int:id_assignment>', views.Assignment.as_view(), name='assignment_for_project'),
    path('projects/<str:slug_project>/clear_sandbox', views.clear_sandbox, name='clear_sandbox'),
    path('projects/<str:slug_project>/ping', views.ping, name='ping'),


    path('api/messages_reject', views.Messages_Reject.as_view(), name='messages_reject'),
    path('api/keywords', views.Keywords.as_view(), name='keywords'),

    path('projects/<str:slug_project>/workers/status_block/<str:id_worker>', views.status_block_for_worker),
    path('projects/<str:slug_project>/workers/increment_counter', views.increment_counter_for_worker),

    path('projects/<str:slug_project>/workers', views.Workers.as_view()),
    path('projects/<str:slug_project>/workers/blocks_hard', views.get_blocks_hard),

    path('projects/<str:slug_project>/workers/<str:id_worker>', views.Worker.as_view()),
    # path('projects/<str:slug_project>/workers/status_block', views.Workers.as_view()),
    path('projects/<str:slug_project>/workers/<str:id_worker>/add_block_soft', views.add_block_soft_for_worker),
    path('projects/<str:slug_project>/workers/<str:id_worker>/remove_block_soft', views.remove_block_soft_for_worker),

    # path('projects/<str:slug_project>/workers/<str:id_worker>/count_assignments', views.set_count_assignments),
])
