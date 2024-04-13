from django.db import models

class Communityy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.BooleanField(default=False)
    privacyPolicy = models.TextField()

    def __str__(self):
        return self.name
