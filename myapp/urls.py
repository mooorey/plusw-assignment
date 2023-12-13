from django.urls import path
from . import views
from django.db import models
from django.shortcuts import render

urlpatterns = [
    path('',views.login, name='login'),
    path('signup', views.register, name='register'),
    path('login-page', views.login, name='login'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home')
 ] 