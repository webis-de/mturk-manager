from django.db import models

class m_Account_Mturk(models.Model):
    name = models.CharField(max_length=200, unique=True)
    key_access = models.CharField(max_length=200)
    key_secret = models.CharField(max_length=200)

class m_Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    template = models.TextField()
    fk_account_mturk = models.ForeignKey('m_Account_Mturk', on_delete=models.SET_NULL, null=True, related_name='projects')

class m_Batch(models.Model):
    name = models.CharField(max_length=200, unique=True)
    fk_project = models.ForeignKey('m_Project', on_delete=models.CASCADE, related_name='batches')

class m_Hit(models.Model):
    fk_batch = models.ForeignKey('m_Batch', on_delete=models.CASCADE, related_name='hits')

class m_Assignment(models.Model):
    fk_hit = models.ForeignKey('m_Hit', on_delete=models.CASCADE, related_name='assignments')
    was_approved = models.BooleanField()
    is_approved = models.BooleanField()

class m_Worker(models.Model):
    name = models.CharField(max_length=200, unique=True)
    fk_assignment = models.ForeignKey('m_Assignment', on_delete=models.CASCADE, related_name='workers')
