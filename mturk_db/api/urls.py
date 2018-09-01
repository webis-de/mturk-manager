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
    path('projects/<str:slug_project>/count_assignments_max_per_worker', views.get_count_assignments_max_per_worker),
    path('projects/<str:slug_project>/count_assignments_max_per_worker/<negint:value>', views.set_count_assignments_max_per_worker),

    path('projects/<str:slug_project>/workers/status_block/<str:id_worker>', views.status_block_for_worker),
    path('projects/<str:slug_project>/workers/increment_counter', views.increment_counter_for_worker),

    path('projects/<str:slug_project>/workers', views.Workers.as_view()),
    # path('projects/<str:slug_project>/workers/status_block', views.Workers.as_view()),
    path('projects/<str:slug_project>/workers/<str:id_worker>/add_block_soft', views.add_block_soft_for_worker),
    path('projects/<str:slug_project>/workers/<str:id_worker>/remove_block_soft', views.remove_block_soft_for_worker),

    path('projects/<str:slug_project>/workers/<str:id_worker>/count_assignments', views.set_count_assignments),
])
