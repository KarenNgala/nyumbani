import errno
from hashlib import new
import re
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, View
from .decorators import tenant_required, landlord_required
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from .models import *
from .forms import *


def home(request):
    current_user = request.user
    apartments = Apartment.objects.all()
    if current_user is not None:
        user =  User.objects.get(pk=current_user.id)
        if user.is_tenant:
            tenant = Tenant.objects.get(user = current_user.id)
            return render(request, 'index.html', {'tenant':tenant, 'apartments':apartments})
        elif user.is_landlord:
            landlord = Landlord.objects.get(user = current_user.id)
            return render(request, 'index.html', {'landlord':landlord, 'apartments':apartments})
        else:
            return render(request, 'index.html', {'apartments':apartments})
    return render(request, 'index.html', {'apartments':apartments})



def  info(request):
    current_user = request.user
    if current_user is not None:
        user =  User.objects.get(pk=current_user.id)
        if user.is_tenant:
            tenant = Tenant.objects.get(user = current_user.id)
            return render(request, 'information.html', {'tenant':tenant})
        elif user.is_landlord:
            landlord = Landlord.objects.get(user = current_user.id)
            return render(request, 'information.html', {'landlord':landlord})
        else:
            return render(request, 'information.html')
    return render(request , 'information.html')    


def List_apartment(request):
    apartments = Apartment.objects.all().order_by('-id')
    current_user = request.user
    if current_user is not None:
        user =  User.objects.get(pk=current_user.id)
        if user.is_tenant:
            tenant = Tenant.objects.get(user = current_user.id)
            return render(request, 'listings.html', {'apartments':apartments, 'tenant':tenant})
        elif user.is_landlord:
            landlord = Landlord.objects.get(user = current_user.id)
            return render(request, 'listings.html', {'landlord':landlord, 'apartments':apartments})
        else:
            return render(request, 'listings.html', {'apartments':apartments})
    return render(request,'listings.html' ,{'apartments':apartments})


def listing(request, apart_id):
    listing = Apartment.objects.get(id=apart_id)
    return render(request,'single_listing.html' ,{'listing':listing})


class SignUpView(TemplateView):
    template_name = 'account/signup.html'


#TENANT views
class TenantSignUpView(CreateView):
    model = User
    form_class = TenantSignUpForm
    template_name = 'account/tenant_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tenant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        return redirect(reverse('tenant_info', kwargs={"user_id": user.id}))


def tenant_info(request, user_id):
    user = User.objects.get(pk=user_id)        
    if request.method == 'POST' and user is not None:
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        new_tenant = Tenant(user=user)
        new_tenant.name = name
        new_tenant.phone_number = phone_number
        new_tenant.save()
        return redirect(reverse('tenant_activate', kwargs={"user_id": user.id}))
    else:
        return render(request, 'tenant/profile_info.html', {'user_id':user_id})



def tenant_activate(request, user_id):
    form = Tenant()
    try:
        user = User.objects.get(pk=user_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and user.is_tenant == True:
        user.is_active = True
        user.save()
        return redirect('account_login')
    else:
        return render(request, 'error/failed.html', {'user':user, 'form':form})


@tenant_required
def edit_profile_tenant(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id)        
    if request.method == 'POST' and user is not None:
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        new_tenant = Tenant(user=user)
        new_tenant.name = name
        new_tenant.phone_number = phone_number
        new_tenant.save()
        return redirect('tenant_profile')
    else:
        return render(request, 'tenant/profile_edit.html')


@tenant_required
def tenant_profile(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    tenant = Tenant.objects.get(user=user)
    return render(request, 'tenant/profile.html', {'tenant':tenant})




#LANDLORD views
class LandlordSignUpView(CreateView):
    model = User
    form_class = LandlordSignUpForm
    template_name = 'account/landlord_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'landlord'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        return redirect(reverse('landlord_info', kwargs={"user_id": user.id}))


def landlord_info(request, user_id):
    user = User.objects.get(pk=user_id)        
    if request.method == 'POST' and user is not None:
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        new_landlord = Landlord(user=user)
        new_landlord.name = name
        new_landlord.phone_number = phone_number
        new_landlord.save()
        return redirect(reverse('landlord_activate', kwargs={"user_id": user.id}))
    else:
        return render(request, 'landlord/profile_info.html', {'user_id':user_id})



def landlord_activate(request, user_id):
    form = Landlord()
    try:
        user = User.objects.get(pk=user_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and user.is_landlord == True:
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('landlord_home')
    else:
        return render(request, 'error/failed.html', {'user':user, 'form':form})


def landlord_listings(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id) 
    landlord = Landlord.objects.get(user=user)
    apartments = Apartment.objects.filter(landlord=landlord).all()
    context={
        'landlord':landlord, 
        'apartments':apartments,
    }
    return render(request, 'landlord/my_listings.html', context)


def landlord_home(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id) 
    landlord = Landlord.objects.get(user=user)
    my_apartments = Apartment.objects.filter(landlord=landlord).all()
    apartments = Apartment.objects.filter(landlord=landlord).count()
    bookings = Booking.objects.all()
    tenants=0
    income=0
    for listing in my_apartments:
        for booking in bookings:
            if booking.room.apartment == listing:
                tenants = tenants+1
    for booking in bookings:
        if booking.room.apartment in my_apartments and ((timezone.now() - booking.start_date) < timedelta(days=30)):
            for info in booking.room.apartment.room_type.all():
                income=income+info.price
    
    context={
        'tenants':tenants,
        'bookings': bookings,
        'landlord':landlord, 
        'apartments':apartments,
        'income':income,
    }
    return render(request, 'landlord/home.html', context)


@landlord_required
def edit_profile_landlord(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id)        
    if request.method == 'POST' and user is not None:
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        new_landlord = Landlord(user=user)
        new_landlord.name = name
        new_landlord.phone_number = phone_number
        new_landlord.save()
        return redirect('landlord_profile')
    else:
        return render(request, 'landlord/profile_edit.html')


@landlord_required
def landlord_profile(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    landlord = Landlord.objects.get(user=user)
    return render(request, 'landlord/profile.html', {'landlord':landlord})
        