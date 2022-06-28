from . import views
from django.urls import include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    re_path(r'^$', views.home, name='index'),

    #TENANT urls
    re_path(r'^tenant/information/(?P<user_id>[0-9]+)/$', views.tenant_info, name='tenant_info'),
    re_path(r'^tenant/activate/(?P<user_id>[0-9]+)/$', views.tenant_activate, name='tenant_activate'),
    re_path(r'^tenant/profile/$', views.tenant_profile, name='tenant_profile'),
    re_path(r'^tenant/edit_profile/$', views.edit_profile_tenant, name='edit_tenant_profile'),

    # LANDLORD uls
    # re_path(r'^landlord/$', views.landlord, name='landlord'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) 
