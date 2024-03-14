from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from customer.models import D_quotation,Customquotation,CustomerDetail#UserProfile
from django.views import View
from .customer_forms import PCBForm
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
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            name=form.cleaned_data['name']
            if not User.objects.filter(username=username).exists():
                # Save the form to create the user
                user = form.save()
                
                # Create a CustomerDetail instance for the user
                customer_detail =CustomerDetail.objects.create(
                    user=user,
                )
                
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')
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
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Customer_entry')  
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request,'customer/customer_login.html', {'form': form})
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
        customer_detail = get_object_or_404(CustomerDetail, user=request.user)
        initial_data = {
            'name': request.user.username,
            'email': request.user.email,  # Assuming email is stored in the User model
        }
        form = PCBForm(initial=initial_data)
        return render(request, 'customer/default_quotation.html', {'form': form})

    def post(self, request):
        global cost
        cost = 0
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
                            print(surface_pad_finish)
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
                            surface_pad_finish=data['surface_pad_finish']
                        )
                        return HttpResponseRedirect(reverse('place_order'))
            elif 'create' in request.POST:
                 cost=calculation()
                 print(cost)
                 current=request.user
                 print(current)
                 return render(request, 'customer/default_quotation.html', {'form': form, 'finall_total_cost': cost})
                
     
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
        customer_detail = get_object_or_404(CustomerDetail, user=request.user)
        initial_data = {
            'name': request.user.username,
            'email': request.user.email,  # Assuming email is stored in the User model
        }
        form = Custom_quotation(initial=initial_data)
        return render(request, 'customer/customized_quotation.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
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

                    message = 'Your quotation request has been submitted. Our staff will contact you via email shortly.'
                    return render(request, 'customer/customized_quotation.html', {'message': message, 'form': form})
            else:
                form = Custom_quotation()

            return render(request, 'customer/customized_quotation.html', {'form': form})
def place_order(request):
     return render(request, 'customer/place_order.html')
@login_required
def your_order(request):
    current_user = request.user
    d_quotations = D_quotation.objects.filter(user=current_user)
    custom_quotations = Customquotation.objects.filter(user=current_user)
    order=list(d_quotations)+list(custom_quotations )
    return render(request, 'customer/your_order.html', {'order': order})
    