from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('workers', views.ViewSet_Workers)
# router.register('projects', views.ViewSet_Projects)

app_name = 'api'
urlpatterns = format_suffix_patterns([
    path('projects/<str:slug_project>/workers/status_block/<str:id_worker>', views.status_block_for_worker),

    path('projects/<str:slug_project>/workers/status_block', views.Workers.as_view()),
    path('projects/<str:slug_project>/workers/<str:id_worker>/add_block_soft', views.add_block_soft_for_worker),
    path('projects/<str:slug_project>/workers/<str:id_worker>/remove_block_soft', views.remove_block_soft_for_worker),
])
