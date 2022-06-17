from . import views
from django.urls import include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    re_path(r'^$', views.home, name='index'),

    #TENANT urls
    # re_path(r'^tenant/profile/$', views.profile, name='profile'),

    # LANDLORD uls
    # re_path(r'^landlord/$', views.landlord, name='landlord'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) 
