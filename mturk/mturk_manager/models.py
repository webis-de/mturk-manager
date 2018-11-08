from django.db import models
# import mturk_manager.classes.workers
from mturk_manager.enums import workers

class Global_DB(models.Model):
    name = models.CharField(max_length=200)
    token_instance = models.CharField(max_length=200)
    token_worker = models.CharField(max_length=200)

# class m_Account_Mturk(models.Model):
#     name = models.CharField(max_length=200, unique=True)
#     key_access = models.CharField(max_length=200)
#     key_secret = models.CharField(max_length=200)   

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = 'MTurk Account'

# class m_Project(models.Model):
#     version = models.IntegerField()
#     name = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(null=False, max_length=200, unique=True)
#     fk_account_mturk = models.ForeignKey('m_Account_Mturk', on_delete=models.SET_NULL, null=True, related_name='projects')
#     title = models.TextField(default='')
#     description = models.TextField(default='')
#     # keywords = models.TextField(default='')
#     count_assignments = models.IntegerField(default=1)
#     reward = models.CharField(default='0.0', max_length=10)
#     lifetime = models.IntegerField(default=604800)
#     duration = models.IntegerField(default=3600)
#     use_sandbox = models.BooleanField(default=True)
#     has_content_adult = models.BooleanField(default=False)

#     # assignments_max_per_worker = models.IntegerField(default=-1)

#     qualification_assignments_approved = models.IntegerField(null=True)
#     qualification_hits_approved = models.IntegerField(null=True)
#     qualification_locale = models.TextField(null=True)
    
#     block_workers = models.BooleanField(default=False)
#     # block_workers = models.CharField(default='disabled', max_length=20)
#     fk_template_main = models.OneToOneField('m_Template', on_delete=models.SET_NULL, null=True, related_name='project')
#     fk_template_assignment_main = models.OneToOneField('m_Template_Assignment', on_delete=models.SET_NULL, null=True, related_name='project')
#     fk_template_hit_main = models.OneToOneField('m_Template_Hit', on_delete=models.SET_NULL, null=True, related_name='project')
#     fk_template_global_main = models.OneToOneField('m_Template_Global', on_delete=models.SET_NULL, null=True, related_name='project')
#     fk_message_reject_default = models.OneToOneField('m_Message_Reject', on_delete=models.SET_NULL, null=True, related_name='project')
#     fk_message_block_default = models.OneToOneField('m_Message_Block', on_delete=models.SET_NULL, null=True, related_name='project')
    
#     keywords = models.ManyToManyField('Keyword', related_name='projects')

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         print('created slug for project {}'.format(self.name))
#         super().save(*args, **kwargs)

#     class Meta:
#         verbose_name = 'Project'

# class m_Batch(models.Model):
#     class Meta:
#         unique_together = ("name", "fk_project")
        
#     name = models.CharField(max_length=200)
#     fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='batches')
#     title = models.TextField()
#     description = models.TextField()
#     keywords = models.ManyToManyField('Keyword', related_name='batches')
#     # keywords = models.TextField()
#     count_assignments = models.IntegerField()
#     use_sandbox = models.BooleanField(default=True)
#     reward = models.CharField(max_length=10)
#     lifetime = models.IntegerField()
#     duration = models.IntegerField()
#     fk_template = models.ForeignKey('m_Template', on_delete=models.CASCADE, related_name='batches', null=True)

# class m_Hit(models.Model):
#     id_hit = models.CharField(max_length=200, unique=True)
#     fk_batch = models.ForeignKey('m_Batch', on_delete=models.CASCADE, related_name='hits')
#     datetime_creation = models.DateTimeField()
#     datetime_expiration = models.DateTimeField()
#     parameters = models.TextField()
#     count_assignments_additional = models.IntegerField(default=0)

# class m_Template(models.Model):
#     class Meta:
#         unique_together = ("name", "fk_project")

#     name = models.CharField(max_length=200)
#     fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='templates')
#     template = models.TextField()
#     height_frame = models.IntegerField()
#     is_active = models.BooleanField(default=True)
#     fk_template_assignment = models.ForeignKey('m_Template_Assignment', on_delete=models.CASCADE, related_name='templates_used')
#     fk_template_hit = models.ForeignKey('m_Template_Hit', on_delete=models.CASCADE, related_name='templates_used')
#     json_dict_parameters = models.TextField()

#     def __str__(self):
#         return self.name

# class m_Template_Assignment(models.Model):
#     class Meta:
#         unique_together = ("name", "fk_project")

#     name = models.CharField(max_length=200)
#     fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='templates_assignment')
#     template = models.TextField()
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

# class m_Template_Hit(models.Model):
#     class Meta:
#         unique_together = ("name", "fk_project")

#     name = models.CharField(max_length=200)
#     fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='templates_hit')
#     template = models.TextField()
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

# class m_Template_Global(models.Model):
#     class Meta:
#         unique_together = ("name", "fk_project")

#     name = models.CharField(max_length=200)
#     fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='templates_global')
#     template = models.TextField()

#     def __str__(self):
#         return self.name

# class m_Assignment(models.Model):
#     class Meta:
#         ordering = ['fk_hit']
#         # order_with_respect_to = 'fk_hit'

#     id_assignment = models.CharField(max_length=200, unique=True, null=False)
#     reviewer_score = models.FloatField(null=True)
#     fk_hit = models.ForeignKey('m_Hit', on_delete=models.CASCADE, related_name='assignments')
#     fk_worker = models.ForeignKey('m_Worker', on_delete=models.CASCADE, related_name='assignments')
#     # was_approved = models.NullBooleanField()
#     # is_approved = models.NullBooleanField()
#     answer = models.TextField()
#     corpus_viewer_tags = models.ManyToManyField('viewer.m_Tag', related_name='corpus_viewer_items')

# class m_Worker(models.Model):
#     class Meta:
#         ordering = ['name']
#         unique_together = ("name", "fk_project")

#     name = models.CharField(max_length=200)
#     fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, null=True, related_name='workers')
#     # is_blocked = models.IntegerField(choices=[(status.value, status.name) for status in workers.STATUS_BLOCK], default=workers.STATUS_BLOCK.NONE.value)
#     # is_blocked_soft = models.BooleanField(default=False)
#     corpus_viewer_tags = models.ManyToManyField('viewer.m_Tag', related_name='corpus_viewer_workers')

# class m_Message_Reject(models.Model):
#     fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='messages_reject')
#     message = models.CharField(max_length=1024)
    
#     def __str__(self):
#         return self.message

# class m_Message_Block(models.Model):
#     fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='messages_block')
#     message = models.TextField()
    
#     def __str__(self):
#         return self.message

# class Model_Qualification(models.Model):
#     id_mturk = models.CharField(max_length=200, unique=True)
#     name = models.CharField(max_length=200, unique=True)
#     description = models.TextField()

# class Keyword(models.Model):
#     text = models.CharField(max_length=200, unique=True)

#     def __str__(self):
#         return self.text