from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField("About", blank=True, null=True)
    title = models.CharField("Title/Profession", max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.user.username

class Role(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.BooleanField(default=False)
    privacyPolicy = models.TextField()
    members = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
    def is_member(self, user):
        return self.members.filter(id=user.id).exists()
    
class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} in {self.community.name} as {self.role.name}'
    
class CommunityTemplate(models.Model):
    template = models.JSONField()
    name = models.CharField(max_length=255,null=True,)
    community = models.ForeignKey(Community,blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Template for Community {self.community}"
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    community = models.ForeignKey(Community,blank=True, null=True, on_delete=models.CASCADE)
    content = models.JSONField(default=dict)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    template = models.ForeignKey(CommunityTemplate, blank=True, null=True, on_delete=models.CASCADE)
    createDate = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)
    user = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE)
    search_vector = SearchVectorField(null=True, editable=False)
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,blank=True, null=True, on_delete=models.CASCADE)
    comment = models.TextField()
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    createdDate = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)
    user = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE)
    search_vector = SearchVectorField(null=True, editable=False)

    def __str__(self):
        return self.comment


class Notification(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    status = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
