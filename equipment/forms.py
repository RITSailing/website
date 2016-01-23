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

    def clean(self, *args, **kwargs):
        cleaned_data = super(EquipmentForm, self).__init__(*args, **kwargs)

# Complete permissions. Tuples for permission levels. Have a method for each permission level that will
# return the user type given the user. Each file and folder will get a permission. RSVP permission for
# events. Filtering events based on permissions. Add permission tuple to main/models.py in the form of
# what is already there.

# Set that up in models. Then talk to Gareth about the implementation of it.

# Event types.