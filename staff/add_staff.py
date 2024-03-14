import re
from django import forms
from django.contrib.auth.models import User
from .models import Staffs
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist

class StaffUserCreationForm(forms.ModelForm):
    username = forms.CharField(label="Username", max_length=100)
    password =forms.CharField(label="Password", widget=forms.PasswordInput)
    name = forms.CharField(label="Name", max_length=100)
    designation = forms.CharField(label="Designation", max_length=100)
    email = forms.EmailField(label="Email")
    phone_number = forms.CharField(label="Phone Number", max_length=10)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)


    class Meta:
        model = Staffs
        fields = ('username', 'email', 'password', 'name', 'designation', 'phone_number')

    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        try:
            Staffs.objects.get(email=email)
            raise forms.ValidationError("This email address is already in use.")
        except ObjectDoesNotExist:
            pass
        
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("This email address is already in use.")
        except ObjectDoesNotExist:
            pass

        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Username is required.")
        if not re.match(r'^\w+$', username):
            raise forms.ValidationError("Username can only contain alphanumeric characters and underscore.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password1 = self.cleaned_data.get("password")
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char in '!@#$%^&*()-_=+[{]};:<>|./?' for char in password1):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password1

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not re.match(r'^[6-9]\d{9}$', phone_number):
            raise forms.ValidationError("Phone number must contain 10 digits and start with 6, 7, 8, or 9.")
        return phone_number

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError("Name is required.")
        if not re.match(r'^[a-zA-Z ]+$', name):
            raise forms.ValidationError("Name must contain only alphabets and spaces.")
        return name

    def clean_designation(self):
        designation = self.cleaned_data.get("designation")
        if not designation:
            raise forms.ValidationError("Designation is required.")
        if not re.match(r'^[a-zA-Z0-9 ]+$', designation):
            raise forms.ValidationError("Designation must contain only alphanumeric characters and spaces.")
        return designation

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        staff = Staffs.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            designation=self.cleaned_data['designation'],
            email=self.cleaned_data['email'],
            phone_number=self.cleaned_data['phone_number']
        )
  
        return staff
