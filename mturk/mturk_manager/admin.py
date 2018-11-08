# from django.contrib import admin
# from mturk_manager.views.settings import update_projects
# from .models import *
# from mturk_manager.views.code_shared import get_url_block_worker
# from django.urls import reverse
# from django.utils.html import format_html

# class MyAdminSite(admin.AdminSite):
#     index_template = 'mturk_manager/admin/index.html'
#     site_header = 'Settings'
#     index_title = None

#     def index(self, request, extra_context=None):
#         extra_context = extra_context or {}
#         # extra_context['url'] = get_url_block_worker(request)
        
#         if request.scheme == 'http':
#             extra_context['url_intern'] = 'http://' + request.get_host()
#         else:
#             extra_context['url_intern'] = 'https://' + request.get_host()

#         return super().index(request, extra_context)

# admin_site = MyAdminSite(name='myadmin')
# # Register your models here.

# class Admin_m_Account_Mturk(admin.ModelAdmin):
#     pass
#     # actions_on_bottom = True

# class Admin_m_Project(admin.ModelAdmin):
#     def update(modeladmin, request, queryset):
#         update_projects(request)
#     update.short_description = "Update selected projects"

#     def mturk_account(self, obj):
#         return obj.fk_account_mturk.name

#     def open(self, obj):
#         return format_html('''
#         <a href="{url}"><i class="fas fa-external-link-alt"></i></a>
#         '''.format(url=reverse('mturk_manager:project', args=(obj.name,))))

#     list_display = ('name', 'mturk_account', 'version', 'open')
#     list_display_links = None
#     actions = [update]

#     class Media:
#         js = ('mturk_manager/js/fontawesome.min.js', 'mturk_manager/js/fa-solid.min.js')





#         # queryset.update(status='p')
#     # actions_on_bottom = True

# admin_site.register(m_Account_Mturk, Admin_m_Account_Mturk)
# admin_site.register(m_Project, Admin_m_Project)
# # admin.site.register(m_Account_Mturk, Admin_m_Account_Mturk)