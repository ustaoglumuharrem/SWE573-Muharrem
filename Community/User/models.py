from django.db import models

# Create your models here.

class User(models.Model):
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    nickName = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
    
