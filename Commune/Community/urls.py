from django.urls import path
from . import views

urlpatterns = [

    path('',views.home,name="home"),
    path('communities',views.all_communities,name="list-communities"),
    path('add_communities/<user_id>',views.add_communities,name="add-communities"),
    path('show_community/<community_id>',views.show_community,name="show-community"),
    path('update_community/<community_id>',views.update_community,name="update-community"),
    path('template',views.template_view,name="template"),
    path('add_post/<template_id>',views.add_post,name="add-post"),
    path('select_template/<community_id>',views.template_get,name="select-template"),
    path('add_userprofile',views.add_userprofile,name="add-userprofile"),
    path('show_userprofile',views.show_userprofile,name="show-userprofile"),
]


