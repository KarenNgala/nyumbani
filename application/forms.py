from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Landlord, Tenant, User,Apartment
from django.db import transaction



class TenantSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(TenantSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ["email", 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_tenant = True
        if commit:
            user.save()
        return user



class LandlordSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(LandlordSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ["email", 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_landlord = True
        if commit:
            user.save()
        return user