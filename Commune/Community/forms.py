
from django.forms import ModelForm
from .models import Community
from .models import UserProfile
from .models import Membership
from .models import Comment
from .models import CommunityTemplate
from .models import Post
from .models import Notification
from .models import Role

class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description', 'type', 'privacyPolicy']

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'about', 'title', 'photo']
        
class MembershipForm(ModelForm):
    class Meta:
        model = Membership
        fields = ['user', 'community', 'role']
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'upvote', 'downvote','template']
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'comment', 'upvote', 'downvote', 'isDeleted', 'updated', 'user']
class CommunityTemplateForm(ModelForm):
    class Meta:
        model = CommunityTemplate
        fields = ['template', 'community']
class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'title', 'message', 'status']
