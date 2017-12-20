from django.urls import path, include, re_path

from . import views

app_name = 'mturk_manager'
urlpatterns = [
    
    path('settings', views.settings, name='settings'),
    path('create', views.create, name='create'),
    path('project/<str:name>', views.project, name='project'),
    path('', views.index, name='index'),
]