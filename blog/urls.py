from django.contrib import admin
from django.urls import path,include
from django.views import generic
from blog.views import (
    BlogDetailView,UserDetailView,Login,home,logout_user,
    register_user,UpdateBlogView,PasswordResetView,BlogListView,
    DeleteBlogView,LikeBlog,AddBlogCreateView,UserProfileView
)
from blog.api.views import BlogViewSet,LoginView,SignUpView, UserProfileApiView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'api-blog', BlogViewSet, basename='blog')


urlpatterns = [
    path('home/',home),
    path('logout',logout_user,name="logout"),
    path('register/',register_user,name='register'),
    path('blogs', BlogListView.as_view(),name='blogs'),
    #path('blog/', blog),
    #path('blogs', blog.as_view(),name='blog'),
    path('password-reset/', PasswordResetView.as_view()),
    path('blog/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    #path('blog/<int:blog_id>',blog_detail,name='blog_detail'),
    path('login', Login.as_view()),
    path('like-blog/<int:pk>', LikeBlog.as_view(), name='like-blog'),
    #path('add_blog', add_blog,name='add_blog'),
    path('add_blog', AddBlogCreateView.as_view(),name='add_blog'),
    #path('delete_blog/<int:id>', delete_blog, name='delete_blog'),
    path('delete_blog/<int:pk>', DeleteBlogView.as_view(), name='delete_blog'),
    path('update_blog/<int:pk>', UpdateBlogView.as_view(),name='update_blog'),
    path('user/<int:pk>',UserDetailView.as_view(),name='user_detail'),
    path('user-profile', UserProfileView.as_view(),name='user_profile'),
    
    
    path('api-login/', LoginView.as_view()),
    path('api-signup/', SignUpView.as_view()),
    path('api-user-profile/', UserProfileApiView.as_view()),


]  + router.urls
