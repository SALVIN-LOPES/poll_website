
from django import views
from django.urls import path,re_path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerPage, name = 'register'),
    path('profile/', views.profilePage, name = 'profile'),
    path('result/', views.getResult, name = 'result'),
    path('create/',views.createPoll, name = 'create'),
    path('poll/<int:id>',views.getPoll, name = 'get_poll'),
    path('', views.home , name='home'),
]

