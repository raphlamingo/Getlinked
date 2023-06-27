from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.find, name='search'),
    path('logout/', views.logoutuser, name='logout_user'),
    path('login/', views.loginuser, name='login_user'),
    path('register/', views.register, name='register'),
    path('opening/', views.new, name='post'),
    path('your_profile/', views.user, name='profile'),
    path('job/<str:pk>', views.post, name='read'),
    path('update/<str:pk>', views.update, name='update'),
    path('delete/<str:pk>', views.delete, name='delete'),
]