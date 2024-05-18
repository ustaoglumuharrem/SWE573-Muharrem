
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
    TYPE_CHOICES = (
        (False, 'Public'),
        (True, 'Private'),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect, initial=False)

    class Meta:
        model = Community
        fields = ['name', 'description', 'type', 'privacyPolicy']

class UserProfileForm(ModelForm):
    photo = forms.URLField(
        label='Photo URL',
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'Enter photo URL'}),
        max_length=100,  # Ensure the max_length matches the database constraint
    )

    class Meta:
        model = UserProfile
        fields = ['nickname', 'about', 'title', 'photo']

    def clean_photo(self):
        photo_url = self.cleaned_data.get('photo')
        if len(photo_url) > 100:
            raise forms.ValidationError("The URL is too long. It should be up to 100 characters.")
        return photo_url
        
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
import datetime
def generate_form(template_json_str):
    template_json = json.loads(template_json_str)
    class DynamicForm(forms.Form):
        title = forms.CharField(label='Title', required=False, max_length=256)
        description = forms.CharField(widget=forms.Textarea, label='Description', required=False)

        latitude = None
        longitude = None

        for field in template_json.get('template', []):
            field_name = field.get('typename')
            field_type = field.get('typefield')
            field_label = field_name.capitalize()

            if field_type == 'text':
                locals()[field_name] = forms.CharField(label=field_label)
            elif field_type == 'image' or field_type == 'video':
                locals()[field_name] = forms.URLField(label=field_label, help_text=f"Enter the URL for the {field_label.lower()}")
            elif field_type == 'email':
                locals()[field_name] = forms.EmailField(label=field_label)
            elif field_type == 'date':
                locals()[field_name] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label=field_label)
            elif field_type == 'number':
                locals()[field_name] = forms.DecimalField(label=field_label)
            elif field_type == 'year':
                locals()[field_name] = forms.IntegerField(min_value=1900, max_value=datetime.date.today().year, label=field_label)
            elif field_type == 'location':
                locals()['latitude'] = forms.FloatField(widget=forms.HiddenInput(), required=False)
                locals()['longitude'] = forms.FloatField(widget=forms.HiddenInput(), required=False)

    return DynamicForm


def generate_dynamic_search_form(template_json_str):
    template_json = json.loads(template_json_str)

    class DynamicSearchForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in template_json.get('template', []):
                field_name = field.get('typename')
                field_label = field.get('typename').capitalize()
                field_type = field.get('typefield')

                if field_type == 'text':
                    self.fields[field_name] = forms.CharField(label=field_label, required=False)
                elif field_type == 'number':
                    self.fields[field_name] = forms.DecimalField(label=field_label, required=False)
                elif field_type == 'email':
                    self.fields[field_name] = forms.EmailField(label=field_label, required=False)
                elif field_type == 'date':
                    self.fields[field_name] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label=field_label)
                elif field_type == 'year':
                    self.fields[field_name] = forms.IntegerField(
                        label=field_label, 
                        required=False, 
                        min_value=1900, 
                        max_value=datetime.date.today().year
                    )

    return DynamicSearchForm

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

