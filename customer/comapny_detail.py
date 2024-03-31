from django import forms
from .models import CustomerDetail

class CompanyForm(forms.ModelForm):
    class Meta:
        model = CustomerDetail
        fields = ['company_name', 'address', 'contact_number']
