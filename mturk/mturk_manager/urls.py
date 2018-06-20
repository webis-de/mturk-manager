from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from mturk_manager import views

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('workers', views.ViewSet_Workers)
# router.register('projects', views.ViewSet_Projects)

app_name = 'mturk_manager'
urlpatterns = format_suffix_patterns([

    # path('api/qualifications/', views.Qualifications.as_view(), name='qualifications'),
    # path('api/qualifications/<str:name>/', views.Qualification.as_view(), name='qualification'),

    # path('api/workers/', views.Workers.as_view(), name='workers'),
    path('api/workers/<str:name>/', views.Worker.as_view(), name='worker'),

    # path('api/projects/', views.Projects.as_view(), name='projects'),
    path('api/projects/<str:slug_project>/', views.Project.as_view(), name='project_api_tmp'),
    path('api/projects/<str:slug_project>/workers/', views.Workers.as_view(), name='workers_for_project'),
    path('api/projects/<str:slug_project>/qualifications/', views.Qualifications.as_view(), name='qualifications_for_project'),
    path('api/projects/<str:slug_project>/qualifications/<str:id_mturk>', views.Qualification.as_view(), name='qualification_for_project'),

    path('view/<str:name>', views.view, name='view'),
    path('documentation', views.documentation, name='documentation'),

    path('settings', views.settings, name='settings'),
    
    path('create', views.create, name='create'),
    path('project/<str:name>/download', views.download, name='download'),

    path('project/<str:name>/api', views.api, name='api'),
    path('project/<str:name>/api/worker/<str:id_worker>', views.api_status_worker, name='api_status_worker'),
    path('project/<str:name>/api/workers', views.api_workers, name='api_workers'),
    path('project/<str:name>/api/assignments_real', views.api_assignments_real, name='api_assignments_real'),
    path('project/<str:name>/api/assignment/<str:id_assignment>', views.api_assignment, name='api_assignment'),
    path('project/<str:name>/api/assignments_fake', views.api_assignments_fake, name='api_assignments_fake'),
    path('project/<str:name>/api/assignments_real_approved', views.api_assignments_real_approved, name='api_assignments_real_approved'),
    path('project/<str:name>/api/assignments_real_approved_tmp', views.api_assignments_real_approved_tmp, name='api_assignments_real_approved_tmp'),
    path('project/<str:name>/api/assignments_real_approved_for_batch/<str:name_batch>', views.api_assignments_real_approved_for_batch, name='api_assignments_real_approved_for_batch'),
    path('project/<str:name>/api/balance', views.balance, name='balance'),
    path('project/<str:name>/api/policies', views.api_policies, name='api_policies'),

    path('project/<str:name>/tmp', views.money, name='money'),

    path('', views.dashboard, name='index'),

    path('project/<str:name>', views.project, name='project'),


])
