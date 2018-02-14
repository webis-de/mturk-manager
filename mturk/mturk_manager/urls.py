from django.urls import path, include, re_path

from . import views

app_name = 'mturk_manager'
urlpatterns = [
    path('view/<str:name>', views.view, name='view'),
    path('documentation', views.documentation, name='documentation'),
    path('settings', views.settings, name='settings'),
    path('create', views.create, name='create'),
    path('project/<str:name>/download', views.download, name='download'),
    path('project/<str:name>/api', views.api, name='api'),
    path('project/<str:name>', views.project, name='project'),
    path('', views.index, name='index'),
]