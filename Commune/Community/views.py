from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.db import models
from .models import Community
from .models import Post
from .models import Comment
from .models import CommunityTemplate
from .models import Notification
from .models import UserProfile
from .forms import CommunityForm
from .forms import CommentForm
from .forms import UserProfileForm
from .models import Membership
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import generate_form
from .forms import PostForm
from django.contrib.auth.models import User
import datetime  # Import the datetime module
from decimal import Decimal
from django.core.files.storage import default_storage
from django.db.models import Q
from .forms import generate_dynamic_search_form
import decimal

def add_userprofile(request):
    submitted = False
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            userprofile = UserProfile(
                nickname=form.cleaned_data['nickname'],
                about=form.cleaned_data['about'],
                title=form.cleaned_data['title'],
                user=request.user
            )
            
            # Handle the photo URL
            photo_url = form.cleaned_data['photo']
            if photo_url:
                userprofile.photo.name = photo_url  # Save URL directly as a string

            userprofile.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = UserProfileForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_userprofile.html', {'form': form, 'submitted': submitted})

def show_userprofile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('add-userprofile')
    
    form = UserProfileForm(request.POST or None, instance=profile)
    
    if request.method == 'POST' and form.is_valid():
        profile.nickname = form.cleaned_data['nickname']
        profile.about = form.cleaned_data['about']
        profile.title = form.cleaned_data['title']

        # Handle the photo URL
        photo_url = form.cleaned_data['photo']
        if photo_url:
            profile.photo.name = photo_url  # Save URL directly as a string

        profile.save()
        return redirect('show-userprofile')
    
    return render(request, 'show_userprofile.html', {'form': form, 'profile': profile})

def show_posts(request,community_id):
    posts = Post.objects.filter(community_id=community_id)  # Fetch all posts
    for post in posts:
        # Check if post.content is a string and convert it to a dictionary
        if isinstance(post.content, str):
            post.content = json.loads(post.content)
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post_id=post.id)
    if isinstance(post.content, str):
        post.content = json.loads(post.content)

    # Instantiate a new comment form
    comment_form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if comment_form.is_valid():
            Comment.objects.create(
                comment=comment_form.cleaned_data['comment'],
                post=post,
                user=request.user
                
            )
            return redirect(request.path_info)  # Refresh the page to display the new comment

    return render(request, 'post_comments_list.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

def upvote_comment(request, comment_id,post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.upvote += 1
    comment.save()
    return redirect('post_detail', post_id=comment.post.id)  # Redirect back to the post containing the comment

def downvote_comment(request, comment_id,post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.downvote += 1
    comment.save()
    return redirect('post_detail', post_id=comment.post.id)  # Redirect back to the post containing the comment

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check user permission to edit comment
    if request.user != comment.user:
        return redirect('post_detail', post_id=comment.post.id)  # Redirect or show an error

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            # Set the 'updated' field to True before saving
            updated_comment = form.save(commit=False)
            updated_comment.updated = True
            updated_comment.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form})

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    template = CommunityTemplate.objects.get(pk=post.template_id)
    FormClass = generate_form(template.template)

    # Initialize the form with the post's existing content data
    initial_data = json.loads(post.content)
    # Extract just the values for form initialization
    initial_values = {key: value['value'] for key, value in initial_data.items()}
    form = FormClass(request.POST or None, request.FILES or None, initial=initial_values)


    if request.method == 'POST' and form.is_valid():
        # Similar logic as in add_post, but now we're updating an existing record
        cleaned_data = {}
        field_types = json.loads(template.template).get('template', [])
        type_mapping = {field['typename']: field['typefield'] for field in field_types}

        for key, value in form.cleaned_data.items():
            field_type = type_mapping.get(key)
            if isinstance(value, datetime.date):
                cleaned_data[key] = {'value': value.isoformat(), 'type': field_type}
            elif isinstance(value, Decimal):
                cleaned_data[key] = {'value': str(value), 'type': field_type}
            elif hasattr(value, 'read'):  # Check if the field is a file upload
                # Save file and categorize based on content type
                file_path = default_storage.save(value.name, value)
                if value.content_type.startswith('image/'):
                    cleaned_data[key] = {'value': file_path, 'type': 'image'}
                elif value.content_type.startswith('video/'):
                    cleaned_data[key] = {'value': file_path, 'type': 'video'}
                else:
                    cleaned_data[key] = {'value': file_path, 'type': 'file'}
            else:
                cleaned_data[key] = {'value': value, 'type': field_type}

        # Update post fields
        post.title = cleaned_data.get('title', {}).get('value', post.title)
        post.description = cleaned_data.get('description', {}).get('value', post.description)
        post.content = json.dumps(cleaned_data)  # Serialize updated data
        post.save()  # Save the updated post

        return redirect('list-communities')  # Redirect or to the detail view of the post

    return render(request, 'edit_post.html', {'form': form, 'post': post})
from django.core.files.uploadedfile import InMemoryUploadedFile

def add_post(request, template_id):
    from django.core.files.storage import default_storage
    from django.shortcuts import redirect, render

    template = CommunityTemplate.objects.get(pk=template_id)
    FormClass = generate_form(template.template)

    form = FormClass(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        latitude = form.cleaned_data.get('latitude')
        longitude = form.cleaned_data.get('longitude')
        cleaned_data = {}
        field_types = json.loads(template.template).get('template', [])
        type_mapping = {field['typename']: field['typefield'] for field in field_types}

        for key, value in form.cleaned_data.items():
            field_type = type_mapping.get(key)
            if isinstance(value, datetime.date):
                cleaned_data[key] = {'value': value.isoformat(), 'type': field_type}
            elif isinstance(value, Decimal):
                cleaned_data[key] = {'value': str(value), 'type': field_type}
            # elif hasattr(value, 'read'):  # Handle file uploads differently
            #     # Generate URL for the file, store URL, and make it clickable
            #     file_url = default_storage.url(default_storage.save(value.name, value))
            #     cleaned_data[key] = {'value': f"<a href='{file_url}' target='_blank'>{file_url}</a>", 'type': field_type}
            else:
                cleaned_data[key] = {'value': value, 'type': field_type}

        new_post = Post.objects.create(
            title=cleaned_data.get('title', {}).get('value', ''),
            description=cleaned_data.get('description', {}).get('value', ''),
            template_id=template.id,
            content=json.dumps(cleaned_data),
            user_id=request.user.id,
            community_id=template.community_id
        )
        return redirect('list-communities')

    return render(request, 'add_post.html', {'form': form, 'template': template})


def create_template(request,community_id):
    if request.method == 'POST':
        # Fetch lists of typename and typefield from POST data
        template_name = request.POST.get('template_name', 'Default Template Name')
        typenames = request.POST.getlist('typename[]')
        typefields = request.POST.getlist('typefield[]')

        # Create a list of dictionaries for each typename and typefield pair
        template_list = [{'typename': tn, 'typefield': tf} for tn, tf in zip(typenames, typefields)]

        # Structure the final JSON to include a "template" key
        template_json = json.dumps({'template': template_list})

        # Create a new template instance and save it
        new_template = CommunityTemplate(name=template_name, template=template_json, community_id=community_id)
        new_template.save()

        # Redirect to another URL (list-communities)
        return redirect('list-communities')

    # Render the form template if not POST request
    return render(request, 'create_template.html',{'community_id': community_id})




def advanced_search_posts(request, template_id):
    template = get_object_or_404(CommunityTemplate, pk=template_id)
    FormClass = generate_dynamic_search_form(template.template)
    form = FormClass(request.GET or None)

    if request.method == 'GET' and form.is_valid():
        posts = Post.objects.filter(template=template)
        print(f"Initial query: {posts}")

        filtered_posts = []
        for post in posts:
            content = json.loads(post.content)
            match = True
            for field, value in form.cleaned_data.items():
                if value:
                    field_type = next((item for item in json.loads(template.template)['template'] if item["typename"] == field), {}).get('typefield')

                    post_value = content.get(field, {}).get('value', '')

                    if field_type == 'date':
                        if isinstance(value, datetime.date):
                            value = value.isoformat()
                        if post_value != value:
                            match = False
                            break
                    elif field_type == 'number':
                        # Compare numerical values directly
                        if isinstance(value, (int, float, decimal.Decimal)) and isinstance(post_value, (int, float, decimal.Decimal)):
                            if value != post_value:
                                match = False
                                break
                    elif field_type in ['email', 'video', 'image']:
                        # Ensure both are strings for comparison
                        if not isinstance(post_value, str):
                            post_value = str(post_value)
                        if not isinstance(value, str):
                            value = str(value)

                        if value.lower() not in post_value.lower():
                            match = False
                            break
                    else:
                        # Ensure both are strings for comparison
                        if not isinstance(post_value, str):
                            post_value = str(post_value)
                        if not isinstance(value, str):
                            value = str(value)

                        if value.lower() not in post_value.lower():
                            match = False
                            break

            if match:
                post.content = content  # Update the post's content with the deserialized JSON
                filtered_posts.append(post)

        print(f"Posts found: {filtered_posts}")

        return render(request, 'advanced_search_results.html', {'form': form, 'posts': filtered_posts})

    return render(request, 'search_form.html', {'form': form, 'template_id': template_id})



def upvote_post(request,post_id,community_id):
    post=Post.objects.get(id=post_id)
    post.upvote = post.upvote+1
    post.save()
    return redirect(reverse('show_posts', kwargs={'community_id': community_id}))

def downvote_post(request,post_id,community_id):
    post=Post.objects.get(id=post_id)
    post.downvote = post.downvote+1
    post.save()
    return redirect(reverse('show_posts', kwargs={'community_id': community_id}))


def template_view(request):
    community_template=CommunityTemplate.objects.get(id=1)
    # template_data = json.loads(community_template.template)  # Parse JSON to dict
    return render(request, 'dynamic_template.html', {'template_data': community_template.template['template']})

def template_get(request,community_id):
    community_templates=CommunityTemplate.objects.filter(community_id=community_id)
    # template_data = json.loads(community_template.template)  # Parse JSON to dict
    return render(request, 'select_template.html',  {'community_templates': community_templates})

def template_advanced_get(request,community_id):
    community_templates=CommunityTemplate.objects.filter(community_id=community_id)
    # template_data = json.loads(community_template.template)  # Parse JSON to dict
    return render(request, 'advanced_search_select_template.html',  {'community_templates': community_templates})
     

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

def add_communities(request, user_id):
    submitted = False
    if request.method == "POST":
        form = CommunityForm(request.POST)
        if form.is_valid():
            created_community = form.save()
            assign_role(user_id, created_community.id, 1)
            
            default_template = CommunityTemplate(
                template='{"template": []}', 
                name="Default Template",
                community=created_community
            )
            default_template.save()
            
            return HttpResponseRedirect('add_communities?submitted=True')
    else:
        form = CommunityForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_community.html', {'form': form, 'submitted': submitted, 'user_id': user_id})

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
    send_kick_notification(user_id,community_id)
    return redirect('list-communities')  # Using 'redirect' shortcut here


def home(request):
    name1="Muharrem"
    notification = Notification.objects.filter(user_id=request.user.id,status=False)
    communities = Community.objects.annotate(member_count=models.Count('members')).order_by('-member_count')
    return render(request, 'home.html', {'communities': communities,'notification':notification})


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


def members_community(request, community_id):
    community = get_object_or_404(Community, pk=community_id)
    memberships = Membership.objects.filter(community=community)

    return render(request, 'show_members.html', {
        'community': community,
        'memberships': memberships,
    })


def send_kick_notification(user_id,community_id):
    community = Community.objects.get(id=community_id)
    
    Notification.objects.create(
        title="You kicked from",
        message=community.name,
        user_id=user_id,
        status=False 

    )
    return redirect('list-communities')  # Using 'redirect' shortcut here

def show_notification(request):
    notifications = Notification.objects.filter(user_id=request.user.id,status=False)
    return render(request,'show_notification.html',{'notifications':notifications})



def search_posts(request):
    query = request.GET.get('q', '')  # Get the query from URL parameter (q)
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        posts = Post.objects.none()  # Return an empty queryset to avoid loading all posts unnecessarily

    return render(request, 'search_results.html', {'posts': posts, 'query': query})


def approve_or_reject_notification(request,notification_id,community_name, answer):
    community = Community.objects.get(name=community_name)
    notification =Notification.objects.get(id=notification_id)
    notification.status=True
    notification.save()
    if answer:
        assign_role(request.user.id,community.id,3)

    return redirect('show_notification')  # Using 'redirect' shortcut here





