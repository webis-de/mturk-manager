from django.db import models
from api.enums import assignments
from datetime import datetime
from django.utils import timezone

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
    datetime_visited = models.DateTimeField(default=timezone.now)
    count_assignments_max_per_worker = models.IntegerField(null=True)
    datetime_creation = models.DateTimeField(default=timezone.now)

    settings_batch_default = models.OneToOneField('Settings_Batch', on_delete=models.SET_NULL, null=True, related_name='project_default')
    
    # block_workers = models.CharField(default='disabled', max_length=20)
    # fk_template_main = models.OneToOneField('m_Template', on_delete=models.SET_NULL, null=True, related_name='project')
    
    # fk_template_assignment_main = models.OneToOneField('m_Template_Assignment', on_delete=models.SET_NULL, null=True, related_name='project')
    # fk_template_hit_main = models.OneToOneField('m_Template_Hit', on_delete=models.SET_NULL, null=True, related_name='project')
    # fk_template_global_main = models.OneToOneField('m_Template_Global', on_delete=models.SET_NULL, null=True, related_name='project')
    message_reject_default = models.ForeignKey('MessageReject', on_delete=models.SET_NULL, null=True, related_name='project')
    # fk_message_block_default = models.OneToOneField('m_Message_Block', on_delete=models.SET_NULL, null=True, related_name='project')
    amount_budget_max = models.IntegerField(null=True)

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
    
    batch = models.OneToOneField('Batch', on_delete=models.CASCADE, null=True, related_name='settings_batch')

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='settings_batch')
    name = models.CharField(max_length=200)

    title = models.TextField(null=True)
    description = models.TextField(null=True)
    reward = models.IntegerField(default=0)
    count_assignments = models.IntegerField(default=1)
    count_assignments_max_per_worker = models.IntegerField(null=True)
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

class Template(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    template = models.TextField()
    is_active = models.BooleanField(default=True)
    datetime_creation = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('project', 'name')
        abstract = True

    def __str__(self):
        return self.name

class Template_Worker(Template):
    height_frame = models.IntegerField()
    template_assignment = models.ForeignKey('Template_Assignment', null=True, on_delete=models.SET_NULL, related_name='templates_used')
    template_hit = models.ForeignKey('Template_HIT', null=True, on_delete=models.SET_NULL, related_name='templates_used')
    template_global = models.ForeignKey('Template_Global', null=True, on_delete=models.SET_NULL, related_name='templates_used')
    json_dict_parameters = models.TextField()

    def __str__(self):
        return self.name

class Template_Assignment(Template):
    pass

# class Template_HIT():
class Template_HIT(Template):
    pass

class Template_Global(Template):
    pass

# class Batch(Settings_Batch):
class Batch(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, related_name='batch')
    name = models.CharField(max_length=200)
    use_sandbox = models.BooleanField()
    datetime_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class HIT(models.Model):
    id_hit = models.CharField(max_length=200, unique=True)
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, null=True, related_name='hits')

    datetime_creation = models.DateTimeField()
    datetime_expiration = models.DateTimeField(db_index=True)
    parameters = models.TextField()
    count_assignments_additional = models.IntegerField(default=0)
    count_assignments_dead = models.IntegerField(default=0)

class Assignment(models.Model):
    id_assignment = models.CharField(max_length=200, unique=True)
    hit = models.ForeignKey('HIT', on_delete=models.CASCADE, related_name='assignments')
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, null=True, related_name='assignments')

    status_external = models.IntegerField(null=True, choices=[(status.value, status.name) for status in sorted(assignments.STATUS_EXTERNAL)])
    status_internal = models.IntegerField(null=True, choices=[(status.value, status.name) for status in sorted(assignments.STATUS_INTERNAL)])
    datetime_creation = models.DateTimeField(default=timezone.now)

    datetime_submit = models.DateTimeField(null=True)
    datetime_accept = models.DateTimeField(null=True)

    answer = models.TextField()


class Message(models.Model):
    message = models.CharField(max_length=1024)
    message_lowercase = models.CharField(max_length=1024, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.message


class MessageReject(Message):
    projects = models.ManyToManyField('Project', related_name='messages_reject')


class MessageApprove(Message):
    projects = models.ManyToManyField('Project', related_name='messages_approve')


class Reason(Message):
    projects = models.ManyToManyField('Project', related_name='messages_reason')


class Worker(models.Model):
    class Meta:
        ordering = ['id_worker']
        # unique_together = ("id_worker", "project")

    id_worker = models.CharField(max_length=200, unique=True)
    is_blocked_global = models.BooleanField(default=False)
    # project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, related_name='workers')

# class Project(models.Model):
#     slug = models.SlugField(null=False, max_length=200, unique=True)
#     count_assignments_max_per_worker = models.IntegerField(default=-1)
    

class Worker_Block_Project(models.Model):
    class Meta:
        pass
        # unique_together = ("project", "worker")
    # is_sandbox = models.BoloeanField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='worker_blocks_project')
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='worker_blocks_project')

class Count_Assignments_Worker_Project(models.Model):
    class Meta:
        unique_together = ("project", "worker")
        
    count_assignments = models.IntegerField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='count_assignments')
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='count_assignments')

# prevents double submissions for same assignment
class Assignment_Worker(models.Model):
    class Meta:
        unique_together = ("id_worker", "id_assignment")

    id_worker = models.CharField(max_length=200)
    id_assignment = models.CharField(max_length=200)


    