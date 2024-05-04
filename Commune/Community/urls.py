from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('',views.home,name="home"),
    path('communities',views.all_communities,name="list-communities"),
    path('add_communities/<user_id>',views.add_communities,name="add-communities"),
    path('show_community/<community_id>',views.show_community,name="show-community"),
    path('show_notification',views.show_notification,name="show_notification"),
    path('update_community/<community_id>',views.update_community,name="update-community"),
    path('all_communities_user/<community_id>',views.all_communities_user,name="all_communities_user"),
    path('join_community/<community_id>',views.join_community,name="join-community"),
    path('remove_community/<community_id>',views.remove_community,name="remove-community"),
    path('remove_user_from_community/<user_id>/<community_id>',views.remove_user_from_community,name="remove_user_from_community"),
    path('template',views.template_view,name="template"),
    path('add_post/<template_id>',views.add_post,name="add-post"),
    path('select_template/<community_id>',views.template_get,name="select-template"),
    path('add_userprofile',views.add_userprofile,name="add-userprofile"),
    path('show_userprofile',views.show_userprofile,name="show-userprofile"),
    path('assign_user_role/<user_id>/<community_id>/<role_id>',views.assign_user_role,name="assign_user_role"),
    path('invite_user/<community_id>',views.invite_user,name="invite_user"),
    path('send_invitation/<user_id>/<community_id>',views.send_invitation,name="send_invitation"),
    path('approve_or_reject_notification/<notification_id>/<community_name>/<answer>',views.approve_or_reject_notification,name="approve_or_reject_notification"),
    path('show_posts/<community_id>',views.show_posts,name="show_posts"),  
    path('create_template',views.create_template,name="create_template"),
]


