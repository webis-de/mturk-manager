from django.db import models

class Account_Mturk(models.Model):
    name = models.CharField(max_length=200, unique=True)
    key_access = models.CharField(max_length=200)
    key_secret = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'MTurk Account'

class Worker(models.Model):
    id_worker = models.CharField(max_length=200, unique=True)

class Project(models.Model):
    slug = models.SlugField(null=False, max_length=200, unique=True)

class Worker_Block_Project(models.Model):
    is_sandbox = models.BooleanField()
    fk_project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='worker_blocks_project')
    fk_worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='worker_blocks_project')

class Count_Assignments_Worker_Project(models.Model):
    count_assignments = models.IntegerField()