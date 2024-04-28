from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Community
from .models import Post
from .models import Comment
from .models import CommunityTemplate
from .models import UserProfile
from .forms import CommunityForm
from .forms import PostForm
from .forms import UserProfileForm
from .models import Membership
import json


def add_userprofile(request):
    submitted =False
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            userprofile=UserProfile(
                nickname=form.cleaned_data['nickname'],
                about=form.cleaned_data['about'],
                title=form.cleaned_data['title'],
                photo=form.cleaned_data['photo'],
                user=request.user
            )
            userprofile.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = UserProfileForm()
        if 'submitted' in request.GET:
                submitted =True
    return render(request,'add_userprofile.html',{ 'form': form, 'submitted':submitted})



def show_userprofile(request):
    try:
        # Attempt to retrieve the UserProfile for the currently logged-in user.
        profile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        # Redirect to add-userprofile page or show a link to create a profile.
        return redirect('add-userprofile')
    
    # Initialize the form either with form data (POST) or with instance data (GET).
    
    form = UserProfileForm(request.POST or None,request.FILES or None , instance=profile)
    
    if request.method == 'POST':
        # Check if the form is valid on submitting.
        if form.is_valid():
            form.save()
            # You might want to redirect to a confirmation page or the same page to show updated data
            return redirect('show-userprofile')  # Assuming 'profile-success' is a valid URL name

    # If GET request or form is not valid, render the same page with the form.
    
    return render(request, 'show_userprofile.html', {'form': form, 'profile': profile})
    


def add_post(request,template_id):
    template=CommunityTemplate.objects.get(id=template_id)
    submitted =False
    if request.method == "POST":
        
        form = PostForm(request.POST)
        if form.is_valid():  
            form.save()
            return HttpResponseRedirect('add_post?submitted=True')
        
    else:
        form = PostForm()
        if 'submitted' in request.GET:
                submitted =True
    return render(request,'add_post.html',{'form':form, 'submitted':submitted,'template':template.template['template']})





def template_view(request):
    community_template=CommunityTemplate.objects.get(id=1)
    # template_data = json.loads(community_template.template)  # Parse JSON to dict
    return render(request, 'dynamic_template.html', {'template_data': community_template.template['template']})

def template_get(request,community_id):
    community_templates=CommunityTemplate.objects.filter(community_id=community_id)
    # template_data = json.loads(community_template.template)  # Parse JSON to dict
    return render(request, 'select_template.html',  {'community_templates': community_templates})
     

def update_community(request,community_id):
    community = Community.objects.get(pk=community_id)
    form = CommunityForm(request.POST or None,instance=community)
    if form.is_valid():
            form.save()
            return redirect('list-communities')
    return render(request,'update_community.html',{"community":community, 'form':form})

def show_community(request,community_id):
    community = Community.objects.get(pk=community_id)
    posts = Post.objects.filter(community=community, isDeleted=False).order_by('-createDate')
    return render(request,'show_community.html',{'community':community,'post':posts})

def add_communities(request,user_id):
    submitted =False
    if request.method == "POST":
        form = CommunityForm(request.POST)
        if form.is_valid():
            created_community=form.save()
            assign_role(user_id,created_community.id,1)
            return HttpResponseRedirect('add_communities?submitted=True')
        
    else:
        form = CommunityForm()
        if 'submitted' in request.GET:
                submitted =True
    return render(request,'add_community.html',{'form':form, 'submitted':submitted,'user_id':user_id})

def all_communities(request):
    community_list = Community.objects.all()
    return render(request,'community_list.html',{"community_list":community_list})


def home(request):
    name1="Muharrem"
    return render(request,'home.html',{"name":name1})


def assign_role(user_id,community_id,role_id):
     Membership.objects.create(
        community_id= community_id,
        user_id=user_id,
        role_id=role_id
     )