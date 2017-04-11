from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from django import forms
from .models import Request
from . import models

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'RIT Email', 'required':'', 'pattern':'[\w.%+-]+@(rit|g\.rit|)\.edu'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name', 'required':'', 'maxlength':"50"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name', 'required':'', 'maxlength':"50"}))
    year_level = forms.ChoiceField(choices=models.YEAR_LEVELS + [('','Year Level')], widget=forms.Select(attrs={'class':'selectpicker show-menu-arrow form-control'}))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data['email']
        if email and 'rit.edu' in email:
            if email.split('@', 1)[1] != 'g.rit.edu':
                cleaned_data['email'] = email.split('@', 1)[0] + '@g.rit.edu'
                email = cleaned_data['email']
        else:
            self._errors["email"] = ["Please enter a valid RIT email."]

        if Request.objects.filter(email=email):
            self._errors["email"] = ["That email has already requested to join."] # Will raise a error message
            del email
        elif User.objects.filter(email=email):
            self._errors["email"] = ["That email is already being used."] # Will raise a error message
            del email

        return cleaned_data

    def save(self, *args, **kwargs):
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        year_level = self.cleaned_data['year_level']
        return Request.objects.create_request(email, first_name, last_name, year_level)

class ProfileForm(forms.Form):
    eboard_pos = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eboard Position', 'maxlength':"50", "aria-describedby":'addon'}))
    phone_number = PhoneNumberField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone Number', "aria-describedby":'addon'}))
    sailing_level = forms.ChoiceField(choices=models.SAILING_LEVELS, widget=forms.Select(attrs={'class':'form-control'}))
    year_level = forms.ChoiceField(choices=models.YEAR_LEVELS, widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        self.member = kwargs.pop('member', None)
        self.is_staff = kwargs.pop('is_staff', False)
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["eboard_pos"].initial = self.member.eboard_pos
        self.fields["phone_number"].initial = self.member.phone_number
        self.fields["sailing_level"].initial = self.member.sailing_level
        self.fields["year_level"].initial = self.member.year_level

    def save(self, *args, **kwargs):
        self.member.eboard_pos = self.cleaned_data['eboard_pos']
        self.member.phone_number = self.cleaned_data['phone_number']
        if self.is_staff:
            self.member.sailing_level = self.cleaned_data['sailing_level']
        self.member.year_level = self.cleaned_data['year_level']
        return self.member.save()
