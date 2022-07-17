from . import views
from django.urls import include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    re_path(r'^$', views.home, name='index'),
    re_path(r'^listings/$', views.List_apartment, name='listings'),
    re_path(r'^info/$', views.info, name='info'),
    re_path(r'^single_listing/(?P<apart_id>[0-9]+)/$', views.listing, name='single_listing'),
    

    #TENANT urls
    re_path(r'^tenant/information/(?P<user_id>[0-9]+)/$', views.tenant_info, name='tenant_info'),
    re_path(r'^tenant/activate/(?P<user_id>[0-9]+)/$', views.tenant_activate, name='tenant_activate'),
    re_path(r'^tenant/profile/$', views.tenant_profile, name='tenant_profile'),
    re_path(r'^tenant/edit_profile/$', views.edit_profile_tenant, name='edit_tenant_profile'),
    re_path(r'^book_room/(?P<apart_id>[0-9]+)/$', views.book_room, name='book_room'),


    # LANDLORD uls
    re_path(r'^landlord/home/$', views.landlord_home, name='landlord_home'),
    re_path(r'^landlord/listings/$', views.landlord_listings, name='landlord_listings'),
    re_path(r'^my_tenants/$', views.my_tenants, name='my_tenants'),
    re_path(r'^new/listing/$', views.new_listing, name='new_listing'),
    re_path(r'^manage/rooms/$', views.manage_rooms, name='manage_rooms'),
    re_path(r'^vacate_room/(?P<booking_id>[0-9]+)/$', views.delete_tenant, name='delete_tenant'),
    re_path(r'^change_status/(?P<booking_id>[0-9]+)/$', views.confirm_payment, name='confirm_payment'),
    re_path(r'^landlord/information/(?P<user_id>[0-9]+)/$', views.landlord_info, name='landlord_info'),
    re_path(r'^landlord/activate/(?P<user_id>[0-9]+)/$', views.landlord_activate, name='landlord_activate'),
    re_path(r'^landlord/profile/$', views.landlord_profile, name='landlord_profile'),
    re_path(r'^landlord/edit_profile/$', views.edit_profile_landlord, name='edit_landlord_profile'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) 
