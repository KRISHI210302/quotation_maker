from django import forms
from django.core.validators import RegexValidator,MinLengthValidator
from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext_lazy as _
def validate_email_com(value):
    if not value.lower().endswith('.com'):
        raise ValidationError('Email must end with .com')
class PCBForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'pattern': '[A-Za-z ]+', 'title': 'Alphabets only'}))
    contact_person = forms.CharField(label='Contact Person', max_length=100, widget=forms.TextInput(attrs={'pattern': '[A-Za-z ]+', 'title': 'Alphabets only'}))
    phone_number = forms.CharField(label='Phone Number', max_length=10, widget=forms.TextInput(attrs={'pattern': '[6-9]\d{9}', 'title': 'Phone number must contain 10 numbers and start with 6, 7, 8, or 9.'}))
    email = forms.EmailField(label='Email',validators=[validate_email_com])
    MATERIAL_CHOICES = [('material 1', 'Material 1'),('material 2', 'Material 2')]
    material = forms.ChoiceField(label='Material', choices=MATERIAL_CHOICES)
    SUBSTRATE_THICKNESS_CHOICES = [
        ('thickness 1', 'Thickness 1'),
        ('thickness 2', 'Thickness 2'),

   
    ]
    substrate_thickness = forms.ChoiceField(label='Substrate Thickness', choices=SUBSTRATE_THICKNESS_CHOICES)
    COPPER_THICKNESS_CHOICES = [
        ('copper 1', 'Copper 1'),
        ('copper 2', 'Copper 2'),
    
    ]
    copper_thickness = forms.ChoiceField(label='Copper Thickness', choices=COPPER_THICKNESS_CHOICES)
    SINGLE_DOUBLE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
    ]
    single_double_side = forms.ChoiceField(label='Single/Double Side', choices=SINGLE_DOUBLE_CHOICES)
    quantity = forms.IntegerField(label='Quantity', min_value=1)
    length = forms.DecimalField(label='Length (cm)', min_value=0)
    breadth = forms.DecimalField(label='Breadth (cm)', min_value=0)
    SURFACE_PAD_FINISH_CHOICES = [
        ('None','None'),
        ('ENIG', 'ENIG'),
        ('HASL', 'HASL'),
        ('PTH', 'PTH'),
        ('Solder', 'Solder'),
        ('Tin coating', 'Tin coating'),
        ('3M tape', '3M tape'),
    
    ]
    surface_pad_finish = forms.ChoiceField(label='Surface Pad Finish', choices=SURFACE_PAD_FINISH_CHOICES)

'''from django import forms
from .models import UserProfile
import re

class UserProfileForm(forms.ModelForm):
    DESIGNATION_CHOICES = (
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
        ('Intern', 'Intern'),
    )

    designation = forms.ChoiceField(choices=DESIGNATION_CHOICES)
    class Meta:
        model = UserProfile
        fields = ['name', 'designation', 'email', 'phone_number', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise forms.ValidationError("Name must contain only alphabets.")
        return name

    def clean_designation(self):
        designation = self.cleaned_data.get('designation')
        if designation not in ['staff1', 'staff2']:
            raise forms.ValidationError("Designation must be either 'staff1' or 'staff2'.")
        return designation

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain 10 digits.")
        return phone_number

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        if not username.isalnum():
            raise forms.ValidationError("Username must contain only letters and numbers.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or len(password) > 12:
            raise forms.ValidationError("Password must be between 8 and 12 characters long.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one capital letter.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char in "!@#$%^&*()-_+=<>,.?/:;{}[]|'\"~`" for char in password):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password'''
