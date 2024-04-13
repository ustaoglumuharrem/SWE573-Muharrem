from django.db import models
from User.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
