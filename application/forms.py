from random import choices
from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .models import *


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


class NewApartment(forms.ModelForm):
    name =  forms.CharField()
    image =  forms.ImageField()
    description =  forms.CharField()
    room_type = forms.ModelMultipleChoiceField(required=False,queryset=RoomType.objects.all(), widget=forms.CheckboxSelectMultiple)
    amenity = forms.ModelMultipleChoiceField(queryset=Amenity.objects.all(),widget=forms.CheckboxSelectMultiple)
    house_rules = forms.ModelMultipleChoiceField(queryset=HouseRule.objects.all(),widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Apartment
        fields = ["name", "description", "image" , "room_type", "amenity", "house_rules"]

    def __init__(self, *args, **kwargs):
        super(NewApartment, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.widget.input_type != 'checkbox':
                visible.field.widget.attrs['class'] = 'form-control'


class ManageRooms(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
    )
    name = forms.CharField()
    is_occupied = forms.ChoiceField(label="Is this room Occupied?", choices=TRUE_FALSE_CHOICES, widget=forms.Select())

    class Meta:
        model = Room
        fields = ["name", "is_occupied"]

    def __init__(self, *args, **kwargs):
        super(ManageRooms, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.widget.input_type != 'radio':
                visible.field.widget.attrs['class'] = 'form-control'
