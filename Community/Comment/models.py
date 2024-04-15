from django.db import models
from Post.models import Post
from User.models import User
from django.contrib.postgres.search import SearchVectorField

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    createdDate = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_vector = SearchVectorField(null=True, editable=False)
