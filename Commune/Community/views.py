from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .models import Community
from .models import Post
from .models import Comment
from .models import CommunityTemplate
from .models import Notification
from .models import UserProfile
from .forms import CommunityForm
from .forms import PostForm
from .forms import UserProfileForm
from .models import Membership
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import generate_form
from django.contrib.auth.models import User



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
    


def add_post(request, template_id):
    template = CommunityTemplate.objects.get(pk=template_id)
    template_data = json.loads(template.template)
    FormClass = generate_form(template_data)
    print("Form fields to render:", FormClass)  # Debugging the form fields

    form = FormClass(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        print("dadadasdasadss")  # Debugging the form fields

        new_post = Post.objects.create(
            community_template=template,
            content=form.cleaned_data
        )
        return redirect('list-communities')
    
    print("Form fields to render:", form.fields)  # Debugging the form fields
    return render(request, 'add_post.html', {'form': form,'template_data':template_data,'template':template})

# def add_post(request, template_id):
#     template = get_object_or_404(CommunityTemplate, id=template_id)
#     submitted = False
#     print(template)
#     print(submitted)
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)  # Include request.FILES for handling file uploads
#         if form.is_valid():
#             new_post = form.save(commit=False)

#             # Create a dictionary from the POST data relevant to the template
#             content_data = {}
#             for field in template.template['template']:
#                 field_name = field['typename']
#                 if field['typefield'] in ['file', 'image']:  # Check if the field is a file or image
#                     file_item = request.FILES.get(field_name)
#                     if file_item:
#                         # Process file saving or handling logic here
#                         # For demonstration, just use the file name, but usually, you would save the file
#                         content_data[field_name] = file_item.name
#                 else:
#                     content_data[field_name] = request.POST.get(field_name, '')

#             # Convert dictionary to JSON
#             json_string = json.dumps(content_data)
#             print(json_string)  # Debugging: Print JSON string to console
            
#             new_post.content = json_string
#             new_post.template = template
#             new_post.user = request.user  # Assuming the user is logged in
#             new_post.save()
            
#             return HttpResponseRedirect('?submitted=True')

#     else:
#         form = PostForm()
#         if 'submitted' in request.GET:
#             submitted = True

#     context = {
#         'form': form,
#         'submitted': submitted,
#         'template': template.template['template']
#     }
#     return render(request, 'add_post.html', context)




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

def changeuserrole_community(request,community_id):
    community = Community.objects.get(pk=community_id)
    form = CommunityForm(request.POST or None,instance=community)
    if form.is_valid():
            form.save()
            return redirect('list-communities')
    return render(request,'change_userrole.html',{"community":community, 'form':form})

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
    user_roles = Membership.objects.filter(user_id=request.user.id)
    
    # Create a list to hold the combined data
    communities_with_roles = []
    
    # Iterate over all communities
    for community in community_list:
        # Initialize with no role
        # user_role_in_community = None
        owner=False
        member=False
        moderator=False
        
        # Check if the current user has a role in the community
        for user_role in user_roles:
            if community.id == user_role.community_id:
                user_role_in_community = user_role.role_id  # assuming 'role' field exists
                if user_role_in_community == 1:
                    owner=True
                elif user_role_in_community == 2:
                    moderator=True
                elif user_role_in_community == 3:
                    member=True


        
        # Create a new dictionary with the combined data
        community_data = {
            'community': community,
            'member':member,
            'moderator':moderator,
            'owner':owner 
            # 'user_role': user_role_in_community
        }
        
        # Append the combined data to the list
        communities_with_roles.append(community_data)
    
    # Pass the combined list to the template
    return render(request, 'community_list.html', {"communities_with_roles": communities_with_roles})


def all_communities_user(request,community_id):

    user_community_roles = Membership.objects.filter(community_id=community_id)
    
    # Create a list to hold the combined data
   
    return render(request, 'change_userrole.html', {"user_community_roles": user_community_roles})


def join_community(request,community_id):
    assign_role(request.user.id,community_id,3)
    return redirect('list-communities')  # Using 'redirect' shortcut here

def remove_community(request, community_id):
    # Attempt to delete the membership
    membership = Membership.objects.get(user_id=request.user.id, community_id=community_id)
    membership.delete()
    return redirect('list-communities')  # Using 'redirect' shortcut here

def remove_user_from_community(request, user_id, community_id):
    # Attempt to delete the membership
    membership = Membership.objects.get(user_id=user_id, community_id=community_id)
    membership.delete()
    return redirect('list-communities')  # Using 'redirect' shortcut here


def home(request):
    name1="Muharrem"
    return render(request,'home.html',{"name":name1})


def assign_role(user_id,community_id,role_id):
     Membership.objects.create(
        community_id= community_id,
        user_id=user_id,
        role_id=role_id
     )

def assign_user_role(request,user_id,community_id,role_id):
     member= Membership.objects.get(user_id=user_id, community_id=community_id)
     member.role_id=role_id
     member.save()
     return redirect('list-communities')  # Using 'redirect' shortcut here

def invite_user(request,community_id):
    users=User.objects.all()
    community_users=Membership.objects.filter(community_id=community_id)
    users_not_community = []
    
    # Iterate over all communities
    for user in users:
        # Initialize with no role
        # user_role_in_community = None

        
        # Check if the current user has a role in the community
        for community_user in community_users:
            is_exist=False
            if user.id == community_user.user_id:
                is_exist=True
                

        if not is_exist:
            users_not_community.append(user)
 
        # Create a new dictionary with the combined data
        
    return render(request, 'invite_user.html', {"users_not_community": users_not_community,"community_id":community_id})

def send_invitation(request,user_id,community_id):
    community = Community.objects.get(id=community_id)
    
    Notification.objects.create(
        title="Invitation",
        message=community.name,
        user_id=user_id,
        status=False 

    )
    return redirect('list-communities')  # Using 'redirect' shortcut here

def show_notification(request):
    notifications = Notification.objects.filter(user_id=request.user.id,status=False)
    return render(request,'show_notification.html',{'notifications':notifications})


def approve_or_reject_notification(request,notification_id,community_name, answer):
    community = Community.objects.get(name=community_name)
    notification =Notification.objects.get(id=notification_id)
    notification.status=True
    notification.save()
    if answer:
        assign_role(request.user.id,community.id,3)

    return redirect('show_notification')  # Using 'redirect' shortcut here






