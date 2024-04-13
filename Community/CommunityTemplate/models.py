from django.db import models
from Communityy.models import Communityy

class CommunityTemplate(models.Model):
    template = models.JSONField()
    community = models.ForeignKey(Communityy, on_delete=models.CASCADE)

    def __str__(self):
        return f"Template for Community {self.communityid}"
