from django.db import models
from Communityy.models import Communityy
from CommunityTemplate.models import CommunityTemplate
from User.models import User
from django.contrib.postgres.search import SearchVectorField
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    community = models.ForeignKey(Communityy, on_delete=models.CASCADE)
    content = models.JSONField()
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    template = models.ForeignKey(CommunityTemplate, on_delete=models.CASCADE)
    createDate = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_vector = SearchVectorField(null=True, editable=False)
    def __str__(self):
        return self.title