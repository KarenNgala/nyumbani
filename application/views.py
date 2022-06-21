import re
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, View
from .decorators import tenant_required, landlord_required
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_text, force_bytes
# from .tokens import account_activation_token
# from django.core.mail import EmailMessage, send_mail
from .models import *
from .forms import *




def home(request):
    # if request.user.is_authenticated:
    #     if request.user.is_counsellor:
    #         return redirect('landlord')
    return render(request, 'index.html')


class SignUpView(TemplateView):
    template_name = 'account/signup.html'

#tenant views
class TenantSignUpView(CreateView):
    model = User
    form_class = TenantSignUpForm
    template_name = 'account/tenant_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tenant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')




#landlord views
class LandlordSignUpView(CreateView):
    model = User
    form_class = LandlordSignUpForm
    template_name = 'account/landlord_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tenant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')

def List_apartment(request):
    apartments = Apartment.objects.all().order_by('-id')
    
    return render(request,'listings.html' ,{'apartments':apartments})


def  info(request):
    return render(request , 'information.html')    