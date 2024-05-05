
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

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), label='Leave a comment')

class CommunityTemplateForm(ModelForm):
    class Meta:
        model = CommunityTemplate
        fields = ['template', 'community']
class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'title', 'message', 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'content']  # Adjust fields based on your Post model

import json
from django import forms

def generate_form(template_json_str):
    template_json = json.loads(template_json_str)
    class DynamicForm(forms.Form):
        title = forms.CharField(label='Title', required=False, max_length=256)
        description = forms.CharField(widget=forms.Textarea, label='Description', required=False)

        # Initialize latitude and longitude as None
        latitude = None
        longitude = None

        for field in template_json.get('template', []):
            field_name = field.get('typename')
            field_type = field.get('typefield')
            field_label = field_name.capitalize()

            # Create fields based on type
            if field_type == 'text':
                locals()[field_name] = forms.CharField(label=field_label)
            elif field_type == 'image':
                locals()[field_name] = forms.ImageField(label=field_label)
            elif field_type == 'email':
                locals()[field_name] = forms.EmailField(label=field_label)
            elif field_type == 'date':
                locals()[field_name] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label=field_label)
            elif field_type == 'number':
                locals()[field_name] = forms.DecimalField(label=field_label)
            elif field_type == 'location':
                # Add latitude and longitude fields only if 'location' type is specified
                locals()['latitude'] = forms.FloatField(widget=forms.HiddenInput(), required=False)
                locals()['longitude'] = forms.FloatField(widget=forms.HiddenInput(), required=False)

    return DynamicForm



class GeoLocationWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(attrs={'placeholder': 'Latitude', 'step': '0.000001'}),
            forms.NumberInput(attrs={'placeholder': 'Longitude', 'step': '0.000001'}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return [None, None]

    def value_from_datadict(self, data, files, name):
        lat = data.get(name + '_0', None)
        lng = data.get(name + '_1', None)
        return ','.join([lat, lng]) if lat and lng else None

