from django import forms

class OrderForm(forms.Form):
    company_name = forms.CharField(max_length=100)
    customer_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=15)
    email=forms.CharField(max_length=20)
    address = forms.CharField(max_length=200,widget=forms.Textarea)
    quantity = forms.IntegerField(min_value=1)
    cost = forms.DecimalField(min_value=0.01, max_digits=10, decimal_places=2)
