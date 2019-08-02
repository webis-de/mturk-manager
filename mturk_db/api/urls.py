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

urlpatterns = format_suffix_patterns([
    path('config', views.Config.as_view(), name='config'),

    path('projects/<str:slug_project>/balance', views.get_balance, name='get_balance'),
    path('projects/<str:slug_project>/finances', views.Finances.as_view(), name='get_finances_for_project'),

    path('projects/<str:slug_project>/templates_worker_all', views.templates_worker_all, name='templates_worker_for_project_all'),
    path('projects/<str:slug_project>/templates_worker', views.Templates_Worker.as_view(), name='templates_for_project'),
    path('projects/<str:slug_project>/templates_worker/<int:id_template>', views.Template_Worker.as_view(), name='template_for_project'),

    path('projects/<str:slug_project>/templates_assignment_all', views.templates_assignment_all, name='templates_assignment_for_project_all'),
    path('projects/<str:slug_project>/templates_assignment', views.Templates_Assignment.as_view(), name='templates_assignment_for_project'),
    path('projects/<str:slug_project>/templates_assignment/<int:id_template>', views.Template_Assignment.as_view(), name='template_assignment_for_project'),

    path('projects/<str:slug_project>/templates_hit_all', views.templates_hit_all, name='templates_hit_for_project_all'),
    path('projects/<str:slug_project>/templates_hit', views.Templates_HIT.as_view(), name='templates_hit_for_project'),
    path('projects/<str:slug_project>/templates_hit/<int:id_template>', views.Template_HIT.as_view(), name='template_hit_for_project'),

    path('projects/<str:slug_project>/templates_global_all', views.templates_global_all, name='templates_global_for_project_all'),
    path('projects/<str:slug_project>/templates_global', views.Templates_Global.as_view(), name='templates_global_for_project'),
    path('projects/<str:slug_project>/templates_global/<int:id_template>', views.Template_Global.as_view(), name='template_global_for_project'),

    # path('projects/<str:slug_project>/settings_batch', views.Settings_Batch.as_view(), name='settings_batch_for_project'),

    path('projects/<str:slug_project>/count_assignments_max_per_worker', views.get_count_assignments_max_per_worker),
    path('projects/<str:slug_project>/count_assignments_max_per_worker/<negint:value>', views.set_count_assignments_max_per_worker),

    ##################################################################
    # Projects
    ##################################################################
    path('info_projects/uniqueness/<str:name_project>', views.projects_check_uniqueness, name='projects_check_uniqueness'),
    path('projects', views.Projects.as_view(), name='projects'),
    path('projects/<str:slug_project>', views.Project.as_view(), name='project'),
    path('projects/<str:slug_project>/clear_sandbox', views.clear_sandbox, name='clear_sandbox'),
    path('projects/<str:slug_project>/ping', views.ping, name='ping'),

    path('projects/<str:slug_project>/tasks', views.Tasks.as_view(), name='tasks_for_project'),
    path('projects/<str:slug_project>/tasks/<int:id_task>', views.Task.as_view(), name='task_for_project'),

    ##################################################################
    # Batches
    ##################################################################
    path('batches', views.Batches.as_view(), name='batches'),

    path('projects/<str:slug_project>/batches', views.ProjectBatches.as_view(), name='batches_for_project'),
    path('projects/<str:slug_project>/batches/<int:id_batch>', views.Batch.as_view(), name='batch_for_project'),
    path('projects/<str:slug_project>/batches_for_annotation', views.batches_for_annotation, name='batches_for_annotation'),
    path('projects/<str:slug_project>/download_batches', views.download_batches, name='download_batches'),
    path('projects/<str:slug_project>/download_info_batches', views.download_info_batches, name='download_info_batches'),
    path('projects/<str:slug_project>/import_batches', views.import_batches, name='import_batches'),

    ##################################################################
    # HITs
    ##################################################################
    path('hits', views.HITs.as_view(), name='hits'),

    path('projects/<str:slug_project>/hits', views.ProjectHITs.as_view(), name='hits_for_project'),
    path('projects/<str:slug_project>/hits_for_annotation', views.hits_for_annotation, name='hits_for_annotation'),
    ##################################################################
    # Assignments
    ##################################################################
    path('assignments', views.Assignments.as_view(), name='assignments'),

    path('projects/<str:slug_project>/assignments', views.ProjectAssignments.as_view(), name='assignments_for_project'),
    path('projects/<str:slug_project>/assignments/<int:id_assignment>', views.ProjectAssignment.as_view(), name='assignment_for_project'),

    path('projects/<str:slug_project>/assignments_for_annotation', views.assignments_for_annotation, name='assignments_for_annotation'),

    ##################################################################
    # Batch Settings
    ##################################################################
    path('projects/<str:slug_project>/settings_batch_all', views.settings_batch_all, name='setting_batch_for_project_all'),
    path('projects/<str:slug_project>/settings_batch', views.Settings_Batch.as_view(), name='settings_batch_for_project'),
    path('projects/<str:slug_project>/settings_batch/<int:id_settings_batch>', views.Setting_Batch.as_view(), name='setting_batch_for_project'),

    ##################################################################
    # Messages
    ##################################################################
    path('messagesReject', views.MessagesReject.as_view(), name='messages_reject'),
    # path('messagesApprove', views.MessagesApprove.as_view(), name='messages_approve'),
    # path('messagesReason', views.MessagesReason.as_view(), name='messages_reason'),

    path('projects/<str:slug_project>/messagesReject', views.ProjectMessagesReject.as_view(), name='messages_reject_for_project'),
    # path('projects/<str:slug_project>/messagesApprove', views.ProjectMessagesReject.as_view(), name='messages_approve_for_project'),
    # path('projects/<str:slug_project>/messagesReason', views.ProjectMessagesReject.as_view(), name='messages_reason_for_project'),

    path('projects/<str:slug_project>/messagesReject/<int:id_message>', views.ProjectMessageReject.as_view(), name='message_reject_for_project'),

    ##################################################################
    # Keywords
    ##################################################################
    path('keywords', views.Keywords.as_view(), name='keywords'),

    path('projects/<str:slug_project>/workers/status_block/<str:id_worker>', views.status_block_for_worker),
    path('projects/<str:slug_project>/workers/increment_counter', views.increment_counter_for_worker),

    path('projects/<str:slug_project>/workers', views.Workers.as_view()),
    path('projects/<str:slug_project>/workers/blocks_hard', views.get_blocks_hard),

    path('projects/<str:slug_project>/workers/<str:id_worker>', views.Worker.as_view()),
    # path('projects/<str:slug_project>/workers/status_block', views.Workers.as_view()),
    path('projects/<str:slug_project>/workers/<str:id_worker>/add_block_soft', views.add_block_soft_for_worker),
    path('projects/<str:slug_project>/workers/<str:id_worker>/remove_block_soft', views.remove_block_soft_for_worker),

    # path('projects/<str:slug_project>/workers/<str:id_worker>/count_assignments', views.set_count_assignments),

    # path('projects/<str:slug_project>/assignments/<int:id_assignment>', views.Assignment.as_view(), name='assignment_for_project'),
])
app_name = 'api'


