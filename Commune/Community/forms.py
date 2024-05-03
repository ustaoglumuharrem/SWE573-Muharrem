
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

def generate_form(template_json):
    class DynamicForm(forms.Form):
        pass  # Start with an empty form class

    # Extract the fields from the template JSON
    # fields = template_json.get('template', [])

    for field in template_json:
        if not isinstance(field, dict):
            continue  # Ensure each field is represented as a dictionary

        field_name = field.get('typename')
        field_type = field.get('typefield')

        # Debug: Print each field's details
        print(f"1Processing field: Name={field_name}, Type={field_type}")

        if field_name and field_type:
            # Determine the form field type based on the 'typefield'
            if field_type == 'text':
                field_class = forms.CharField(label=field_name.capitalize())
            elif field_type == 'image':
                field_class = forms.ImageField(label=field_name.capitalize())
            elif field_type == 'location':
                # Example: Use a text input for location; customize as needed
                field_class = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter location'}), label=field_name.capitalize())
            else:
                print(f"Unsupported field type: {field_type}")
                continue

            # Add the field to the form
            setattr(DynamicForm, field_name, field_class)
            print(f"Field added: {field_name} of type {field_type}")

    # Debug: List all fields added to the form class
    print(f"Form fields added: {list(DynamicForm.base_fields)}")
    
    return DynamicForm

