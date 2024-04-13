from django.db import models

# Create your models here.
class Role(models.Model):
    roleName = models.CharField(max_length=100)
    isActive = models.BooleanField(default=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rolename