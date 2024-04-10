from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from urllib.parse import urlencode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from customer.models import D_quotation,Customquotation,CustomerDetail#UserProfile
from django.views import View
from .customer_forms import PCBForm
from .order  import OrderForm
from .customized_quotation import Custom_quotation 
from decimal import Decimal
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings
from .customer_login import LoginForm
from .register import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from  django.contrib.auth.mixins import LoginRequiredMixin
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
from django.contrib.auth.decorators import login_required
import razorpay

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
           
            if not User.objects.filter(username=username).exists():
                # Save the form to create the user
                user = form.save()
                Users = User.objects.get(username=username)
                customer_detail =CustomerDetail.objects.create(
                    user=user,
                    customer_name=username,
                    email=email
                )
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('users_login')
            else:
                messages.error(request, f'{username} is already registered as a customer.')
        else:
            # If the form is invalid, display error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'customer/customer_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if User.objects.filter(username=username).exists():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('Defalut')
                else:
                    form.add_error(None, "Invalid username or password.")
            else:
                form.add_error(None, "User does not exist.")
    else:
        form = LoginForm()
  
    return render(request,'customer/customer_login.html', {'form': form})

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
            return redirect('users_login')  # Redirect to login page after sending reset link
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
                return redirect('users_login')
            else:
                print('Form errors:', form.errors)
        else:
            form = SetPasswordForm(user)

        return render(request, 'customer/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('users_login')
def home(request):
    return render(request,'customer/home.html')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class Customer_entry1(LoginRequiredMixin,View):
    def get(self, request):
        customer_detail = CustomerDetail.objects.filter(user=request.user)
        quotation_no=D_quotation.objects.all()
        initial_data = {
            'contact_person': request.user.username,
            'email': request.user.email,  # Assuming email is stored in the User model
        }
        form = PCBForm(initial=initial_data)
        return render(request, 'customer/default_quotation.html', {'form': form})

    def post(self, request):
        global cost
        cost = 0
        try:
            customer_detail = CustomerDetail.objects.get(user=request.user)
        except CustomerDetail.DoesNotExist:
                customer_detail = None
        form = PCBForm(request.POST) 
        name=request.POST['name'],
        phone_number= request.POST['phone_number']
        material = request.POST['material']
        substrate_thickness = request.POST['substrate_thickness']
        copper_thickness = request.POST['copper_thickness']
        single_double_side = request.POST['single_double_side']
        quantity = Decimal(request.POST.get('quantity'))
        surface_pad_finish = request.POST['surface_pad_finish']
        length = Decimal(request.POST.get('length'))
        breadth = Decimal(request.POST.get('breadth'))
        def calculation():
                    area = (length + Decimal('0.5')) * (breadth + Decimal('0.5'))
                    material_cost = settings.MATERIAL_COSTS[material]  
                    copper_thickness_cost = settings.COPPER_THICKNESS_COSTS[copper_thickness] 
                    substrate_thickness_cost = settings.SUBSTRATE_THICKNESS_COSTS[substrate_thickness]  # Retrieve substrate thickness cost
                    SURFACE_PAD_FINISH_COSTS_TYPE1 = settings.SURFACE_PAD_FINISH_COSTS['type1']
                    SURFACE_PAD_FINISH_COSTS_TYPE2 = settings.SURFACE_PAD_FINISH_COSTS['type2']
                    pcb_cost = settings.SINGLE_SIDED_PCB_COST if single_double_side == 'single' else settings.DOUBLE_SIDED_PCB_COST  # Determine PCB cost based on single/double side
                    surface_pad_finish_cost = 0
                    option=0
                    if data['surface_pad_finish']!='None':
                            option=1
                            surface_pad_finish_cost =settings.SURFACE_PAD_FINISH_COSTS.get(data['surface_pad_finish'], 0)
                    total_cost = Decimal(material_cost + copper_thickness_cost + substrate_thickness_cost +
                                    pcb_cost + surface_pad_finish_cost) * area
                    total_cost=round(total_cost,0)
                    num_pieces_per_panel = settings.PANEL_SIZE / area

                        # Calculate panel order quantity
                    panel_order_quantity = ceil(data['quantity'] / num_pieces_per_panel)
                    setup=settings.SETUP_TIME 
                        # Calculate total hours for order quantity
                    total_hours_order_quantity =setup + (panel_order_quantity * settings.SINGLE_SIDED_PCB_TIME )

                        # Calculate per piece time
                    per_piece_time = total_hours_order_quantity / data['quantity']
                    OVERHEAD_COST=30
                        # Calculate cost per piece
                    cost_single_piece = OVERHEAD_COST * per_piece_time

                        # Calculate material overhead per piece
                    material_oh_per_piece = Decimal(cost_single_piece) + total_cost

                        # Calculate profit
                    profit = Decimal('0.1') * material_oh_per_piece

                        # Calculate overall estimated cost
                    overall_estimated_cost = profit + material_oh_per_piece

                        # Calculate final estimated cost
                    final_estimated_cost = overall_estimated_cost / Decimal('0.1')
                    final_estimated_cost=round( final_estimated_cost,0)
                        # Calculate shipping cost
                    shipping_cost = final_estimated_cost * Decimal('0.1')
                    shipping_cost=round(shipping_cost,0)
                        # Calculate estimated substrate cost per piece
                    estimated_substrate_cost_pc = area * total_cost
                    if option :
                        surface_pad_finish_c = data['surface_pad_finish']
                        cost=0
                        # Calculate option-specific costs

                        if surface_pad_finish_c in settings.SURFACE_PAD_FINISH_COSTS.get('type1', {}):
                            cost = shipping_cost + final_estimated_cost + total_cost
                        elif surface_pad_finish_c in settings.SURFACE_PAD_FINISH_COSTS.get('type2', []):
                            cost = shipping_cost + final_estimated_cost
                    else:
                        cost=shipping_cost +total_cost
                    return(cost)
        
        if form.is_valid():
            data = form.cleaned_data
            co=calculation()
            if 'save' in request.POST:
                    if D_quotation.objects.filter(
                        user=request.user,
                        name=data['name'],
                        contact_person=data['contact_person'],
                        phone_number=data['phone_number'],
                        email=data['email'],
                        material=data['material'],
                        substrate_thickness=data['substrate_thickness'],
                        copper_thickness=data['copper_thickness'],
                        single_double_side=data['single_double_side'],
                        quantity=data['quantity'],
                        length=data['length'],
                        breadth=data['breadth'],
                        surface_pad_finish=data['surface_pad_finish']
                    ).exists():
                        message = "Data already exists with this quotation number and name."
                        return render(request, 'customer/default_quotation.html', {'form': form, 'message': message})
                    else:
                       
                        pcb = D_quotation.objects.create(
                            user=request.user,
                            name=data['name'],
                            contact_person=data['contact_person'],
                            phone_number=data['phone_number'],
                            email=data['email'],
                            material=data['material'],
                            substrate_thickness=data['substrate_thickness'],
                            copper_thickness=data['copper_thickness'],
                            single_double_side=data['single_double_side'],
                            quantity=data['quantity'],
                            length=data['length'],
                            breadth=data['breadth'],
                            surface_pad_finish=data['surface_pad_finish'],
                            cost=co
                        )
                        quotation=D_quotation.objects.get(
                            user=request.user,
                            name=data['name'],
                            contact_person=data['contact_person'],
                            phone_number=data['phone_number'],
                            email=data['email'],
                            material=data['material'],
                            substrate_thickness=data['substrate_thickness'],
                            copper_thickness=data['copper_thickness'],
                            single_double_side=data['single_double_side'],
                            quantity=data['quantity'],
                            length=data['length'],
                            breadth=data['breadth'],
                            surface_pad_finish=data['surface_pad_finish'],
                            cost=co
                        )
                        q_no=quotation.quotation_number
                        if customer_detail:
                            customer_detail.total_orders += 1
                            customer_detail.save()
                        redirect_url = reverse('place_order')+ f'?q_no={q_no}'
                        return HttpResponseRedirect(redirect_url)
            elif 'create' in request.POST:
                 cost=calculation()
                 current=request.user
                 print(current)
                 return render(request, 'customer/default_quotation.html', {'form': form, 'finall_total_cost': co})
            elif 'viewpdf' in request.POST:
                if form.is_valid():
                    c=calculation()
                    print(name,phone_number,material,substrate_thickness,copper_thickness,single_double_side,quantity,surface_pad_finish,cost)
                    data2={
                            'name':name[0], 
                            'phone_number':phone_number,
                            'material':material,
                            'substrate_thickness':substrate_thickness,
                            'copper_thickness':copper_thickness,
                            'single_double_side':single_double_side,
                            'quantity':quantity,
                            'surface_pad_finis':surface_pad_finish,
                            'cost':c,
                            'setup':60
                            }
                  
                    pdf = render_to_pdf('customer/pdf_template.html', data2)
                    return HttpResponse(pdf, content_type='application/pdf')
        else:
            
            return render(request, 'customer/default_quotation.html', {'form': form, 'message': None})
  
        return render(request, 'customer/default_quotation.html', {'form': form, 'message': None})
  
def display_customer_entries(request):
    entries = D_quotation.objects.all()
    return render(request, 'customer/customer_entry.html', {'entries': entries})

class customized_quotation(LoginRequiredMixin, View):
    def get(self, request):
        customer_detail = CustomerDetail.objects.filter(user=request.user)
        initial_data = {
            'contact_person': request.user.username,
            'email': request.user.email,  # Assuming email is stored in the User model
        }
        customer_detail, created = CustomerDetail.objects.get_or_create(user=request.user)
        form = Custom_quotation(initial=initial_data)
        return render(request, 'customer/customized_quotation.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            try:
                customer_detail = CustomerDetail.objects.get(user=request.user)
            except CustomerDetail.DoesNotExist:
                customer_detail = None

            current_user = request.user
            form = Custom_quotation(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if Customquotation.objects.filter(
                        user=request.user,
                        name=form.cleaned_data['name'],
                        contact_person=form.cleaned_data['contact_person'],
                        phone_number=form.cleaned_data['phone_number'],
                        email=form.cleaned_data['email'],
                        material=form.cleaned_data['material'],
                        substrate_thickness=form.cleaned_data['substrate_thickness'],
                        copper_thickness=form.cleaned_data['copper_thickness'],
                        single_double_side=form.cleaned_data['single_double_side'],
                        quantity=form.cleaned_data['quantity'],
                        length=form.cleaned_data['length'],
                        breadth=form.cleaned_data['breadth'],
                        delivery_date=form.cleaned_data['delivery_date'],  # Ensure 'delivery_date' is in form.cleaned_data
                        description=form.cleaned_data['description']
                        

                ).exists():
                    message = "Data already exists with this quotation number and name."
                    return render(request, 'customer/customized_quotation.html', {'form': form, 'message': message})
                else:
                    custom_quote = Customquotation(
                        user=request.user,
                        name=form.cleaned_data['name'],
                        contact_person=form.cleaned_data['contact_person'],
                        phone_number=form.cleaned_data['phone_number'],
                        email=form.cleaned_data['email'],
                        material=form.cleaned_data['material'],
                        substrate_thickness=form.cleaned_data['substrate_thickness'],
                        copper_thickness=form.cleaned_data['copper_thickness'],
                        single_double_side=form.cleaned_data['single_double_side'],
                        quantity=form.cleaned_data['quantity'],
                        length=form.cleaned_data['length'],
                        breadth=form.cleaned_data['breadth'],
                        delivery_date=form.cleaned_data['delivery_date'],  # Ensure 'delivery_date' is in form.cleaned_data
                        description=form.cleaned_data['description']
                    )
                    custom_quote.save()
                    if customer_detail:
                        customer_detail.total_orders += 1
                        customer_detail.save()

                    message = 'Your quotation request has been submitted. Our staff will contact you via email shortly.'
                    return render(request, 'customer/customized_quotation.html', {'message': message, 'form': form})
            else:
                form = Custom_quotation()

            return render(request, 'customer/customized_quotation.html', {'form': form})

class place_order(LoginRequiredMixin, View):
    def get(self, request):
        q_no = request.GET.get('q_no')
        customer_detail = CustomerDetail.objects.filter(user=request.user)
        D_quoat= D_quotation.objects.get(quotation_number=q_no)
        initial_data = {
            'company_name':D_quoat.name,
            'contact_number':D_quoat.phone_number,
            'cost':D_quoat.cost,
            'quantity':D_quoat.quantity,
            'customer_name': request.user.username,
            'email': request.user.email,  # Assuming email is stored in the User model
        }
        form = OrderForm(initial=initial_data)  # Create your additional details form

        return render(request, 'customer/place_order.html', {'form': form,'q_no':q_no})
    def post(self, request):
        form = OrderForm(request.POST)
        if request.method == 'POST':  
            q_no = request.GET.get('q_no')
            b=request.POST['cost']
            amount=int(float(b))*100
            client = razorpay.Client(auth=('rzp_test_OLxlRJQcC6Edsp','tE8qgoxZrgUDdW6aXwf7Mmwx'))
            response_payement=client.order.create(dict(amount=amount,currency='INR'))
            order_id=response_payement['id']
            order_status=response_payement['status']
            if order_status =='created':
                tc=Transaction(amount=amount,order_id=order_id,quo=q_no)
                tc.save()
            
            print(response_payement)
            d={'form': form, 'q_no': q_no,'amount':amount,'order_id':order_id}
            print(d)
            try:
                customer_detail = CustomerDetail.objects.get(company_name=request.POST['company_name'])
                D_quoat= D_quotation.objects.get(quotation_number=q_no)
            except CustomerDetail.DoesNotExist:
                customer_detail = None
                D_quoat = None
            if customer_detail is not None:
              customer_detail.company_name=request.POST['company_name']
              customer_detail.contact_number=request.POST['contact_number']
              customer_detail.address=request.POST['address']
              customer_detail.save()
              print(b)
            return render(request, 'customer/place_order copy.html',context=d)
    
        return render('customer/place_order.html',{'form':form,'q_no':q_no,'amount':amount,'order_id':order_id})
@login_required
def your_order(request):
    current_user = request.user
    print(current_user)
    d_quotations = D_quotation.objects.filter(user=current_user)
    custom_quotations = Customquotation.objects.filter(user=current_user)
    order=list(d_quotations)+list(custom_quotations )
    return render(request, 'customer/your_order.html', {'order': order})

@csrf_exempt
def payment_success(request):
    print('llll')
    response=request.POST
    params_dict ={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }
    client=razorpay.Client(auth=(('rzp_test_OLxlRJQcC6Edsp','tE8qgoxZrgUDdW6aXwf7Mmwx')))
    try:
        status=client.utility.verify_payment_signature(params_dict)
        tcs=Transaction.objects.get(order_id=response['razorpay_order_id'])
        tcs.payment_id=response['razorpay_payment_id']
        tcs.status='paid'
        tcs.paid=True
        tcs.save()
        d_quotations = D_quotation.objects.get(quotation_number=tcs.quo)
        d_quotations.payment_status='paid'
        d_quotations.save()
        return render(request,'customer/payement_success.html',{'status':True})
    except:
        return render(request,'customer/payment_failed.html',{'status':True})

def payment_failed(request):
    return render(request,'customer/payment_failed.html')