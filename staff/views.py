from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from customer.models import CustomerDetail,D_quotation,Customquotation
from .add_staff import StaffUserCreationForm
from django.contrib import messages
from staff.models import Staffs,CustomCreation
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .custom_create_quote import CustomCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from django.contrib.auth.decorators import login_required

god=None
def customer_details(request):
    addstaff =  CustomerDetail.objects.all()
    li_staffs = {"add_staff":addstaff}
    return render(request,'staff_management/customer_details.html',context=li_staffs)

def staff_customer_details(request):
    addstaff =  CustomerDetail.objects.all()
    li_staffs = {"add_staff":addstaff}
    return render(request,'staff_management/staffcustomdetail.html',context=li_staffs)

def add_staff(request):
    form = StaffUserCreationForm()

    if request.method == 'POST':
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            # Extract form data
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
                if username == 'admin':
                 return redirect('home')
                else:
                    return redirect('staff_home')
            else:
                messages.error(request, 'Invalid username or password.')
            god=username
            print(god)
    return render(request, 'staff_management/staff_login.html')
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = 'http://' + current_site.domain + reset_link
            message = render_to_string('customer/forgot_password_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            email = EmailMessage(mail_subject, message, to=[email])
            email.send()
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('staff_login')  # Redirect to login page after sending reset link
        else:
            messages.error(request, 'Email address not found.')
    return render(request, 'customer/forgot_password.html')

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                print('Form is valid')
                form.save()
                messages.success(request, 'Your password has been reset successfully. You can now log in with your new password.')
                return redirect('staff_login')
            else:
                print('Form errors:', form.errors)
        else:
            form = SetPasswordForm(user)

        return render(request, 'customer/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('staff_login')

def staff_details(request):
    staff_profiles = Staffs.objects.all()
    li_staffs = {"add_staff":staff_profiles}
    return render(request,'staff_management/staff_detail.html',context=li_staffs)

def Order_details(request):
    customer_entries =D_quotation.objects.all()
    custom_quotations = Customquotation.objects.all()
    combined_data = list(customer_entries) + list(custom_quotations)
    li_staffs = {"order":combined_data}
    return render(request,'staff_management/orders.html',context=li_staffs)
def staff_Order_details(request):
    customer_entries =D_quotation.objects.all()
    custom_quotations = Customquotation.objects.all()
    combined_data = list(customer_entries) + list(custom_quotations)
    li_staffs = {"order":combined_data}
    return render(request,'staff_management/staff_orders.html',context=li_staffs)


def Home(request):
    return render(request, 'staff_management/admin_home.html')
def staff_home(request):
    return render(request,'staff_management/staff_home.html')

def staff_custom_orders(request):
      entries = Customquotation.objects.all()
      return render(request, 'staff_management/staff_custom_quotation.html', {'entries': entries})
def custom_orders(request):
      entries = Customquotation.objects.all()
      return render(request, 'staff_management/custom_quotation.html', {'entries': entries})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

def send_email_with_pdf(pdf_content, recipient_email):
    subject = 'Your Custom Creation Form'
    message = 'Please find the attached Custom Creation Form.'
    email = EmailMessage(subject, message, 'kavyarajangam21@gmail.com', [recipient_email])
    email.attach('custom_creation_form.pdf', pdf_content, 'application/pdf')
    email.send()

def custom_create(request, entry_id):
    entry = get_object_or_404(Customquotation, pk=entry_id)
    custom_creation = None
    print(entry.email,entry.name)
    initial_data = {
            'quotation_number':entry.quotation_number,
            'email': entry.email,
            'name': entry.name,
        }
    try:
        custom_creation = CustomCreation.objects.get(quotation_number=entry.quotation_number)
        
        form = CustomCreationForm(request.POST or None, instance=custom_creation, initial=initial_data)
    except CustomCreation.DoesNotExist:
        form = CustomCreationForm(request.POST or None,initial=initial_data)

    if request.method == 'POST':
        if form.is_valid():
            if 'submit' in request.POST:
                custom_creation = form.save(commit=False)
                custom_creation.total_charge = custom_creation.calculate_total_charge()
                custom_creation.save()
                return render(request, 'staff_management/custom_create.html', {'form': form, 'entry': entry, 'charge': custom_creation.total_charge if custom_creation else None})  # Redirect to success page or wherever appropriate
            elif 'Email' in request.POST:
                try: 
                    customq = CustomCreation.objects.filter(quotation_number=entry.quotation_number)
                    pdf_content = render_to_pdf('staff_management/custom_pdf_template.html', {'form': form, 'custom_creations': customq})  
                    if pdf_content:
                        send_email_with_pdf(pdf_content.getvalue(), entry.email)  # Pass the PDF content as bytes
                        entry.quotation_status = 'sent'
                        entry.save()
                        return HttpResponse(pdf_content.getvalue(), content_type='application/pdf')  # Return PDF as HttpResponse
                except CustomCreation.DoesNotExist:
                    messages.error(request, 'Quotation does not exist')
    return render(request, 'staff_management/custom_create.html', {'form': form, 'entry': entry, 'charge': custom_creation.total_charge if custom_creation else None})

def staff_custom_create(request, entry_id):
    entry = get_object_or_404(Customquotation, pk=entry_id)
    custom_creation = None
    print(entry.email,entry.name)
    initial_data = {
            'quotation_number':entry.quotation_number,
            'email': entry.email,
            'name': entry.name,
        }
    try:
        custom_creation = CustomCreation.objects.get(quotation_number=entry.quotation_number)
        
        form = CustomCreationForm(request.POST or None, instance=custom_creation, initial=initial_data)
    except CustomCreation.DoesNotExist:
        form = CustomCreationForm(request.POST or None,initial=initial_data)

    if request.method == 'POST':
        if form.is_valid():
            if 'submit' in request.POST:
                custom_creation = form.save(commit=False)
                custom_creation.total_charge = custom_creation.calculate_total_charge()
                custom_creation.save()
                return render(request, 'staff_management/staff_custom_create.html', {'form': form, 'entry': entry, 'charge': custom_creation.total_charge if custom_creation else None})  # Redirect to success page or wherever appropriate
            elif 'Email' in request.POST:
                try: 
                    customq = CustomCreation.objects.filter(quotation_number=entry.quotation_number)
                    pdf_content = render_to_pdf('staff_management/custom_pdf_template.html', {'form': form, 'custom_creations': customq})  
                    if pdf_content:
                        send_email_with_pdf(pdf_content.getvalue(), entry.email)  # Pass the PDF content as bytes
                        entry.quotation_status = 'sent'
                        entry.save()
                        return HttpResponse(pdf_content.getvalue(), content_type='application/pdf')  # Return PDF as HttpResponse
                except CustomCreation.DoesNotExist:
                    messages.error(request, 'Quotation does not exist')
    return render(request, 'staff_management/staff_custom_create.html', {'form': form, 'entry': entry, 'charge': custom_creation.total_charge if custom_creation else None})
def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']
        try:
            df = pd.read_excel(excel_file)  # Assuming you're using pandas to handle Excel files

            for index, row in df.iterrows():
                
                data = {
                    'id': row.get('id'),
                    'customer_name': row.get('customer_name'),
                    'company_name': row.get('company_name'),
                    'address':row.get('address'),
                    'contact_number': row.get('contact_number'),
                    'email': row.get('email'),
                    'total_orders': row.get('total_orders'),
                    'cancel_orders': row.get('cancel_orders'),
                    'delivered_orders': row.get('delivered_orders'),
                    
                }

                # Create a new instance of your model with the extracted data
                user, created = User.objects.get_or_create(username=row.get('username'))  # Assuming 'username' column in Excel contains unique usernames

                # Create a new instance of your model with the extracted data
                instance = CustomerDetail(user=user, **data)
                instance.save()

            return JsonResponse({'message': 'File uploaded successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return render(request, 'staff_management/upload_excel.html')