
from django.forms import ModelForm
from .models import Community
from .models import UserProfile
from .models import Membership
from .models import Comment
from .models import CommunityTemplate
from .models import Post
from .models import Notification
from .models import Role
from django import forms
import json
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
        fields = ['title', 'content', 'community']
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


def generate_form(template_json_str):
    template_json = json.loads(template_json_str)
    class DynamicForm(forms.Form):
        title = forms.CharField(label='Title', required=False, max_length=256)
        description = forms.CharField(widget=forms.Textarea, label='Description', required=False)
        
        for field in template_json.get('template', []):
            field_name = field.get('typename')
            field_type = field.get('typefield')
            
            if field_name and field_type:
                field_label = field_name.capitalize()
                if field_type == 'text':
                    locals()[field_name] = forms.CharField(label=field_label)
                elif field_type == 'image':
                    locals()[field_name] = forms.ImageField(label=field_label)
                elif field_type == 'location':
                    locals()[field_name] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter location'}), label=field_label)
                elif field_type == 'email':
                    locals()[field_name] = forms.EmailField(label=field_label)
                elif field_type == 'date':
                    locals()[field_name] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label=field_label)
                elif field_type == 'number':
                    locals()[field_name] = forms.DecimalField(label=field_label)

    return DynamicForm
