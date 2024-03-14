from django.shortcuts import render,redirect
from customer.models import CustomerDetail
from .add_staff import StaffUserCreationForm
from django.contrib import messages
from staff.models import Staffs
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def customer_details(request):
    addstaff =  CustomerDetail.objects.all()
    li_staffs = {"add_staff":addstaff}
    return render(request,'staff_management/customer_details.html',context=li_staffs)

def add_staff(request):
    form = StaffUserCreationForm()

    if request.method == 'POST':
        print('no')
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            # Extract form data
            print('kkkk')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            designation = form.cleaned_data['designation']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            # Create a new User instance
            user = User.objects.create_user(username=username, password=password)
            
            # Create a new Staffs instance and associate it with the created user
            staff = Staffs.objects.create(
                user=user,
                name=name,
                designation=designation,
                email=email,
                phone_number=phone_number
            )
            print(user,staff)

            messages.success(request, 'Staff registered successfully.')
            return redirect('staff_login')
    
    # If form is not valid, display the errors
    else:
        error_messages = form.errors.values()
        print("error")
        for error in error_messages:
            messages.error(request, error)

    return render(request, 'staff_management/staff_register.html', {'form': form})
   
def staff_login(request):
    if request.method == 'POST':
       form = AuthenticationForm(request, request.POST)
       if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

        # Query the Staff table for the username
            try:
                staff = Staffs.objects.get(user__username=username)
            except Staffs.DoesNotExist:
                staff = None

            # Check if staff exists and if the provided password matches
            if staff and check_password(password, staff.user.password):
                # Set session variable to indicate user is logged in
                request.session['logged_in_user'] = username
                return redirect('staff_detail')
            else:
                messages.error(request, 'Invalid username or password.')
        
    return render(request, 'staff_management/staff_login.html')

def staff_details(request):
    staff_profiles = Staffs.objects.all()
    li_staffs = {"add_staff":staff_profiles}
    return render(request,'staff_management/staff_detail.html',context=li_staffs)
