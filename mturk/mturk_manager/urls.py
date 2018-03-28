from django.urls import path, include, re_path
from django.contrib import admin

from . import views

app_name = 'mturk_manager'
urlpatterns = [
    path('view/<str:name>', views.view, name='view'),
    path('documentation', views.documentation, name='documentation'),

    path('settings', views.settings, name='settings'),
    
    path('create', views.create, name='create'),
    path('project/<str:name>/download', views.download, name='download'),

    path('project/<str:name>/api', views.api, name='api'),
    path('project/<str:name>/api/worker/<str:id_worker>', views.api_status_worker, name='api_status_worker'),
    path('project/<str:name>/api/assignments_real_approved', views.api_assignments_real_approved, name='api_assignments_real_approved'),
    path('project/<str:name>/api/balance', views.balance, name='balance'),

    path('project/<str:name>', views.project, name='project'),
    path('', views.dashboard, name='index'),


]