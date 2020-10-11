from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/signup',views.user_signup,name="signup"),
    path('/create_post',views.post_creation,name="create_post"),
    path('/like_post',views.post_like,name="like_post"),
    path('/unlike_post',views.post_unlike,name="unlike_post"),
    path('/clear_tables',views.clear_tables,name="clear_tables"),
]