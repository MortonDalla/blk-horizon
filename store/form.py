from django import forms
from .models import *

class DistributionsForm(forms.ModelForm):
    class Meta:
        model = Distributions
        fields = [
            'user', 'title', 'company_name', 'email_adress', 'contact_numbers', 'category', 'quantity',
            'description', 'address', 'province', 'city', 'zipcode',
            'date_added'
        ]