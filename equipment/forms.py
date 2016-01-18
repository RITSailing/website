from django import forms
from django.db import models
from . import models

class EquipmentForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    

    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        return ""