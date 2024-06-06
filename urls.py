from django.urls import path
from . import views

urlpatterns = [
  path('home/',views.home,name='home'),
  path('add_blog/',views.add_blog,name='add_blog'),
  path('edit_blog/<int:id>/',views.blog_edit,name='blog_edit'),
  path('delete_blog/<int:id>/',views.blog_delete,name='blog_delete'),
  path('view_blog/<int:id>/',views.blog_view,name='blog_view'),
  path('delete_comment/<int:id>/',views.delete_comment,name='delete_comment'),
  path('edit_comment/<int:id>/',views.edit_comment,name='edit_comment'),

  # user
  path('register/',views.user_register,name='register'),
  path('',views.user_login,name='login'),
  path('logout/',views.user_logout,name='logout'),
  path('profile/',views.profile_add,name='profile'),
  path('profile/view/',views.profile_view,name='profile_view'),
  path('edit/profile/<int:id>/',views.edit_profile,name='edit_profile'),

  # forms
  path('post/blog/',views.post_blog,name='post_blog'),
  path('forgot/password/',views.forgot_password,name='forgot_password'),
  path('verify/password/<str:username>/',views.verify_password,name='verify_password'),
  path('set/new/password/<int:id>/',views.set_new_password,name='set_password'),
]