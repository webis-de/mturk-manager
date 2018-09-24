from django.db import models
from api.enums import assignments
from datetime import datetime

class Account_Mturk(models.Model):
    name = models.CharField(max_length=200, unique=True)
    key_access = models.CharField(max_length=200)
    key_secret = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'MTurk Account'

class Project(models.Model):
    version = models.IntegerField()
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    fk_account_mturk = models.ForeignKey('Account_Mturk', on_delete=models.SET_NULL, null=True, related_name='projects')
    datetime_visited = models.DateTimeField(default=datetime.now)

    settings_batch_default = models.OneToOneField('Settings_Batch', on_delete=models.SET_NULL, null=True, related_name='project_default')
    
    # block_workers = models.CharField(default='disabled', max_length=20)
    # fk_template_main = models.OneToOneField('m_Template', on_delete=models.SET_NULL, null=True, related_name='project')
    
    # fk_template_assignment_main = models.OneToOneField('m_Template_Assignment', on_delete=models.SET_NULL, null=True, related_name='project')
    # fk_template_hit_main = models.OneToOneField('m_Template_Hit', on_delete=models.SET_NULL, null=True, related_name='project')
    # fk_template_global_main = models.OneToOneField('m_Template_Global', on_delete=models.SET_NULL, null=True, related_name='project')
    # fk_message_reject_default = models.OneToOneField('m_Message_Reject', on_delete=models.SET_NULL, null=True, related_name='project')
    # fk_message_block_default = models.OneToOneField('m_Message_Block', on_delete=models.SET_NULL, null=True, related_name='project')
    

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     print('created slug for project {}'.format(self.name))
    #     super().save(*args, **kwargs)

    # class Meta:
    #     verbose_name = 'Project'

class Settings_Batch(models.Model):
    class Meta:
        unique_together = ('project', 'name')

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='settings_batch')

    name = models.CharField(max_length=200)

    title = models.TextField(null=True)
    description = models.TextField(null=True)
    reward = models.CharField(default='0.0', max_length=10)
    count_assignments = models.IntegerField(default=1)
    count_assignments_max_per_worker = models.IntegerField(default=-1)
    lifetime = models.IntegerField(default=604800)
    duration = models.IntegerField(default=3600)
    template_worker = models.ForeignKey('Template_Worker', on_delete=models.SET_NULL, null=True, related_name='settings_batch')
    block_workers = models.BooleanField(default=False)
    
    keywords = models.ManyToManyField('Keyword', related_name='projects')

    has_content_adult = models.BooleanField(default=False)
    qualification_assignments_approved = models.IntegerField(null=True)
    qualification_hits_approved = models.IntegerField(null=True)
    qualification_locale = models.TextField(null=True)

class Keyword(models.Model):
    text = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.text

class Template_Worker(models.Model):
    class Meta:
        unique_together = ('project', 'name')

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='templates_worker')
    name = models.CharField(max_length=200)
    template = models.TextField()
    height_frame = models.IntegerField()
    is_active = models.BooleanField(default=True)
    template_assignment = models.ForeignKey('Template_Assignment', null=True, on_delete=models.SET_NULL, related_name='templates_used')
    template_hit = models.ForeignKey('Template_Hit', null=True, on_delete=models.SET_NULL, related_name='templates_used')
    json_dict_parameters = models.TextField()

    def __str__(self):
        return self.name

class Template_Assignment(models.Model):
    class Meta:
        unique_together = ('project', 'name')

    name = models.CharField(max_length=200)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='templates_assignment')
    template = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Template_Hit(models.Model):
    class Meta:
        unique_together = ('project', 'name')

    name = models.CharField(max_length=200)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='templates_hit')
    template = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name










class Worker(models.Model):
    id_worker = models.CharField(max_length=200, unique=True)

# class Project(models.Model):
#     slug = models.SlugField(null=False, max_length=200, unique=True)
#     count_assignments_max_per_worker = models.IntegerField(default=-1)
    

class Worker_Block_Project(models.Model):
    is_sandbox = models.BooleanField()
    fk_project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='worker_blocks_project')
    fk_worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='worker_blocks_project')

class Count_Assignments_Worker_Project(models.Model):
    class Meta:
        unique_together = ("fk_project", "fk_worker")
        
    count_assignments = models.IntegerField()
    fk_project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='count_assignments')
    fk_worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='count_assignments')

class Assignment_Worker(models.Model):
    class Meta:
        unique_together = ("id_worker", "id_assignment")

    id_worker = models.CharField(max_length=200)
    id_assignment = models.CharField(max_length=200)

class Assignment(models.Model):
    id_assignment = models.CharField(max_length=200, unique=True)
    status_external = models.IntegerField(choices=[(status.value, status.name) for status in assignments.STATUS_EXTERNAL])
    status_internal = models.IntegerField(null=True, choices=[(status.value, status.name) for status in assignments.STATUS_INTERNAL])
    datetime_update = models.DateTimeField(auto_now=True)

    