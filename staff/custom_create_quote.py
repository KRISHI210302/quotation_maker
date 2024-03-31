from django import forms
from .models import CustomCreation

class CustomCreationForm(forms.ModelForm):
    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="Email")
    class Meta:
        model = CustomCreation
        exclude = ['total_charge']
    