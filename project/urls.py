"""nyumbani URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path
from application import views

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'', include('application.urls')),
    re_path('^accounts/', include('allauth.urls')),
    re_path(r'^accounts/signup/$', views.SignUpView.as_view(), name='account_signup'),
    re_path('^accounts/signup/tenant/', views.TenantSignUpView.as_view(), name='tenant_register'),
    re_path('accounts/signup/landlord/', views.LandlordSignUpView.as_view(), name='landlord_signup'),
]