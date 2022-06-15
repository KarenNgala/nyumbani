from django.contrib import admin
from django.urls import path
from application import views

urlpatterns = [
    
    path('home/', views.index),
    
]
