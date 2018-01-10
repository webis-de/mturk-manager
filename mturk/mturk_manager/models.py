from django.db import models

class m_Account_Mturk(models.Model):
    name = models.CharField(max_length=200, unique=True)
    key_access = models.CharField(max_length=200)
    key_secret = models.CharField(max_length=200)

class m_Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    fk_account_mturk = models.ForeignKey('m_Account_Mturk', on_delete=models.SET_NULL, null=True, related_name='projects')
    title = models.TextField(default='')
    description = models.TextField(default='')
    keywords = models.TextField(default='')
    count_assignments = models.IntegerField(default=1)
    reward = models.CharField(default='0.0', max_length=10)
    lifetime = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    fk_template_main = models.OneToOneField('m_Template', on_delete=models.SET_NULL, null=True, related_name='project')
    fk_template_assignment_main = models.OneToOneField('m_Template_Assignment', on_delete=models.SET_NULL, null=True, related_name='project')

class m_Batch(models.Model):
    class Meta:
        unique_together = ("name", "fk_project")
        
    name = models.CharField(max_length=200)
    fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='batches')
    title = models.TextField()
    description = models.TextField()
    keywords = models.TextField()
    count_assignments = models.IntegerField()
    reward = models.CharField(max_length=10)
    lifetime = models.IntegerField()
    duration = models.IntegerField()
    fk_template = models.ForeignKey('m_Template', on_delete=models.CASCADE, related_name='batches')

class m_Hit(models.Model):
    id_hit = models.CharField(max_length=200, unique=True)
    fk_batch = models.ForeignKey('m_Batch', on_delete=models.CASCADE, related_name='hits')
    parameters = models.TextField()

class m_Template(models.Model):
    class Meta:
        unique_together = ("name", "fk_project")

    name = models.CharField(max_length=200)
    fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='templates')
    template = models.TextField()
    height_frame = models.IntegerField()
    is_active = models.BooleanField(default=True)
    fk_template_assignment = models.ForeignKey('m_Template_Assignment', on_delete=models.CASCADE, related_name='templates_used')
    fk_template_hit = models.ForeignKey('m_Template_Hit', on_delete=models.CASCADE, related_name='templates_used')

class m_Template_Assignment(models.Model):
    class Meta:
        unique_together = ("name", "fk_project")

    name = models.CharField(max_length=200)
    fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='templates_assignment')
    template = models.TextField()
    is_active = models.BooleanField(default=True)

class m_Template_Hit(models.Model):
    class Meta:
        unique_together = ("name", "fk_project")

    name = models.CharField(max_length=200)
    fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='templates_hit')
    template = models.TextField()
    is_active = models.BooleanField(default=True)

class m_Assignment(models.Model):
    class Meta:
        ordering = ['fk_hit']
        # order_with_respect_to = 'fk_hit'

    id_assignment = models.CharField(max_length=200, unique=True, null=False)
    fk_hit = models.ForeignKey('m_Hit', on_delete=models.CASCADE, related_name='assignments')
    fk_worker = models.ForeignKey('m_Worker', on_delete=models.CASCADE, related_name='assignments')
    was_approved = models.NullBooleanField()
    is_approved = models.NullBooleanField()
    answer = models.TextField()

class m_Worker(models.Model):
    name = models.CharField(max_length=200, unique=True)
