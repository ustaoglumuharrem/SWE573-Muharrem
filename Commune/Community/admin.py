from django.contrib import admin
from .models import Community
from .models import UserProfile
from .models import Membership
from .models import Comment
from .models import CommunityTemplate
from .models import Post
from .models import Notification
from .models import Role
# Register your models here.


admin.site.register(Community)
admin.site.register(UserProfile)
admin.site.register(Membership)
admin.site.register(CommunityTemplate)
admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Role)