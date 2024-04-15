from django.db import models

from User.models import User
from Communityy.models import Communityy

class UserCommunityy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Communityy, on_delete=models.CASCADE)
    role=models.IntegerField()
    isActive = models.BooleanField(default=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"
        unique_together = ("user", "community")  # Ensure uniqueness of user-community pair

    def __str__(self):
        return f"User: {self.user.username}, Community: {self.community.name}, Role: {self.role}"