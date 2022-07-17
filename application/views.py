from distutils.log import error
import errno
from hashlib import new
import re
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, View
from .decorators import tenant_required, landlord_required
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from .models import *
from .forms import *


def home(request):
    current_user = request.user
    apartments = Apartment.objects.all()
    rooms = Room.objects.filter(status='Available').all()
    if current_user is not None:
        user =  User.objects.get(pk=current_user.id)
        if user.is_tenant:
            tenant = Tenant.objects.get(user = current_user.id)
            return render(request, 'index.html', {'tenant':tenant, 'apartments':apartments, 'rooms':rooms,})
        elif user.is_landlord:
            landlord = Landlord.objects.get(user = current_user.id)
            return render(request, 'index.html', {'landlord':landlord, 'apartments':apartments, 'rooms':rooms,})
        else:
            return render(request, 'index.html', {'apartments':apartments, 'rooms':rooms,})
    return render(request, 'index.html', {'apartments':apartments, 'rooms':rooms,})



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
    current_user = request.user
    rooms = Room.objects.filter(status='Available', apartment=listing).count()
    available_rooms = Room.objects.filter(status='Available', apartment=listing).all()
    room_types = set()
    for room in available_rooms:
        room_types.add(room.room_type)
    if current_user is not None:
        user =  User.objects.get(pk=current_user.id)
        if user.is_tenant:
            tenant = Tenant.objects.get(user = current_user.id)
            return render(request, 'single_listing.html', {'listing':listing, 'tenant':tenant, 'rooms':rooms, 'room_types':room_types})
        elif user.is_landlord:
            landlord = Landlord.objects.get(user = current_user.id)
            return render(request, 'single_listing.html', {'landlord':landlord, 'listing':listing, 'rooms':rooms, 'room_types':room_types})
        else:
            return render(request, 'single_listing.html', {'listing':listing, 'rooms':rooms, 'room_types':room_types})
    return render(request,'single_listing.html' ,{'listing':listing, 'rooms':rooms, 'room_types':room_types})


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
    my_bookings = Booking.objects.filter(tenant=tenant).all()
    current_booking = []
    for booking in my_bookings:
        if booking.end_date > timezone.now():
            current_booking.append(booking)
    context = {
        'tenant':tenant,
        'my_bookings':my_bookings,
        'current_booking':current_booking,
        }
    return render(request, 'tenant/profile.html', context)


@tenant_required
def book_room(request, apart_id):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    tenant = Tenant.objects.get(user=user)
    listing = Apartment.objects.get(pk=apart_id)
    available_rooms = Room.objects.filter(apartment=listing, status='Available').all()

    print(available_rooms)
    context = {
        'tenant':tenant,
        'listing':listing,
        'available_rooms': available_rooms,
    }

    if request.method == 'POST':
        room = request.POST.get('room')
        this_room = Room.objects.get(pk=room)
        this_room.status = 'Pending'
        this_room.save()
        upload = Booking(room=this_room)
        upload.tenant = tenant
        upload.save()
        return redirect('tenant_profile')
    else:
        return render(request, 'tenant/book_room.html', context)


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
    bookings = Room.objects.filter(status='Paid').all()
    rooms = Room.objects.all()
    context={
        'landlord':landlord, 
        'apartments':apartments,
        'bookings':bookings,
        'rooms':rooms,
    }
    return render(request, 'landlord/my_listings.html', context)


def new_listing(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id) 
    landlord = Landlord.objects.get(user=user)
    if request.method == 'POST':
        form = NewApartment(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.landlord = landlord
            form.save()
            return redirect('landlord_listings')
        else:
            return redirect('new_listing')
    else:
        form = NewApartment()
        context = {
        'landlord':landlord, 
        'form':form
        }
        return render(request, 'landlord/new_listing.html', context)   


def manage_rooms(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id) 
    landlord = Landlord.objects.get(user=user)
    apartments = Apartment.objects.filter(landlord=landlord).all()
    room_type = RoomType.objects.all()
    status = [c[0] for c in Room.status.field.choices]

    if request.method == 'POST':
        room_name = request.POST.get('name')
        apartment_id = request.POST.get('apartment')
        this_apartment = Apartment.objects.get(pk=apartment_id)
        room_type_id = request.POST.get('room_type')
        this_room_type = RoomType.objects.get(pk=room_type_id)
        this_status = request.POST.get('status')
        upload = Room(name=room_name, apartment=this_apartment, room_type=this_room_type, status=this_status)
        upload.save()
        return redirect('landlord_home') 
    else:
        context = {
        'landlord':landlord, 
        'apartments':apartments,
        'room_type':room_type,
        'status':status,
        }
        return render(request, 'landlord/manage_rooms.html', context)   

@landlord_required
def my_tenants(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id) 
    landlord = Landlord.objects.get(user=user)
    apartments = Apartment.objects.filter(landlord=landlord).all()
    all_bookings = Booking.objects.all()
    all_status = [c[0] for c in Room.status.field.choices]
    my_bookings = []
    for booking in all_bookings:
        if booking.room.apartment in apartments:
            my_bookings.append(booking)
    context = {
        'landlord':landlord,
        'apartments':apartments,
        'my_bookings':my_bookings,
        'all_status':all_status,
    }
    return render(request, 'landlord/my_tenants.html', context)


@landlord_required
def delete_tenant(request, booking_id):
    booking = Booking.objects.filter(pk=booking_id)
    room = Room.objects.get(id=booking.room.id)
    room.status = 'Available'
    room.save()
    booking.delete()
    return redirect('my_tenants')


@landlord_required
def confirm_payment(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    room = Room.objects.get(id=booking.room.id)
    if room.status == 'Paid':
        room.status = 'Pending'
    elif room.status == 'Pending':
        room.status = 'Paid'
    room.save()
    return redirect('my_tenants')


@landlord_required
def landlord_home(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id) 
    landlord = Landlord.objects.get(user=user)
    my_apartments = Apartment.objects.filter(landlord=landlord).all()
    apartments = Apartment.objects.filter(landlord=landlord).count()
    bookings = Booking.objects.all()
    rooms = Room.objects.filter(status='Available').count()
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
        'rooms':rooms
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
        