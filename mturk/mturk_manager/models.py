from django.db import models

class m_MTurk(models.Model):
    name = models.CharField(max_length=200, unique=True)
    key_access = models.CharField(max_length=200)
    key_secret = models.CharField(max_length=200)

class m_Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    template = models.TextField()
