from django.contrib import admin
from django.urls import path
from application import views

urlpatterns = [
    
    path('home/', views.index),
    path('nav/', views.navbar),
    path('photo/', views.photo),
    path('login/', views.login),
    path('signup/', views.signup),
 
    ]