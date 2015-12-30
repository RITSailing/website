from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django import forms
from models import Request
import models

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'RIT Email', 'required':'', 'pattern':'[\w.%+-]+@(rit|g\.rit|)\.edu'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name', 'required':'', 'maxlength':"50"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name', 'required':'', 'maxlength':"50"}))
    choices = models.YEAR_LEVELS
    choices.insert(0, ('','Year Level'))
    year_level = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class':'selectpicker show-menu-arrow form-control'}))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data['email']
        if Request.objects.filter(email=email):
            self._errors["email"] = ["That email has already requested to join."] # Will raise a error message
            del email
        elif User.objects.filter(email=email):
            self._errors["email"] = ["That email is already being used."] # Will raise a error message
            del email
        elif email and email.split('@', 1)[1] != 'g.rit.edu':
            cleaned_data['email'] = email.split('@', 1)[0] + '@g.rit.edu'
        return cleaned_data

    def save(self):
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        year_level = self.cleaned_data['year_level']
        return Request.objects.create_request(email, first_name, last_name, year_level)
