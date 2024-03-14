from django.db import models
from datetime import datetime
from django.db.models import Max
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator, MaxLengthValidator
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, EmailValidator
'''
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registered_app = models.CharField(default='customer', max_length=100) 

    def __str__(self):
        return f"Name: {self.user}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created :
        UserProfile.objects.create(user=instance, registered_app='customer')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance, registered_app='customer')'''


class PasswordValidator:
    @staticmethod
    def validate_password(value):
        if not any(char.islower() for char in value):
            raise ValidationError('Password must contain at least one lowercase alphabet.')

        if not any(char.isupper() for char in value):
            raise ValidationError('Password must contain at least one uppercase letter.')

        if not any(char.isdigit() for char in value):
            raise ValidationError('Password must contain at least one numeric digit.')

        special_characters = "!@#$%^&*()-_+=<>?/[]{}|"
        if not any(char in special_characters for char in value):
            raise ValidationError('Password must contain at least one special character.')
    
class QuotationNumberGenerator(models.Model):
    @staticmethod
    def generate_quotation_number():
        # Generate a new quotation number based on the current date and next available ID
        base_quotation_number = datetime.now().strftime("%Y%m%d")
        try:
            # Get the last generated quotation numbers from Customer_entry and Custom_Quotation
            last_customer_entry = D_quotation.objects.last()
            last_custom_quotation = Customquotation.objects.last()
        except D_quotation.DoesNotExist:
            last_customer_entry = None
        except Customquotation.DoesNotExist:
            last_custom_quotation = None

        if last_customer_entry and last_custom_quotation:
            if last_customer_entry.id > last_custom_quotation.id:
                last_generated_quotation = last_customer_entry.quotation_number
            else:
                last_generated_quotation = last_custom_quotation.quotation_number
        elif last_customer_entry:
            last_generated_quotation = last_customer_entry.quotation_number
        elif last_custom_quotation:
             last_generated_quotation = last_custom_quotation.quotation_number
        else:
            # If no entries in either model, start with ID 1
            last_generated_quotation = f"{base_quotation_number}-0000"

        # Increment the ID part by 1
        parts = last_generated_quotation.split('-')
        last_counter = int(parts[1]) + 1

        new_quotation_number = f"{base_quotation_number}-{last_counter:04d}"
        return new_quotation_number

class D_quotation(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    quotation_number = models.CharField(max_length=20,unique=True,default=QuotationNumberGenerator.generate_quotation_number, editable=False)
    name = models.CharField(max_length=100, verbose_name='Name', validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Name must contain only alphabets and spaces')])
    contact_person = models.CharField(max_length=100, verbose_name='Contact Person', validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Contact person must contain only alphabets and spaces')])
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number', validators=[RegexValidator(regex='^[0-9]*$', message='Phone number must contain only numbers')])
    email = models.EmailField(verbose_name='Email')
    MATERIAL_CHOICES = [
        ('material 1', 'Material 1'),
        ('material 2', 'Material 2'),
       
    ]
    material = models.CharField(max_length=100, choices=MATERIAL_CHOICES, verbose_name='Material')
    SUBSTRATE_THICKNESS_CHOICES = [
        ('thickness 1', 'Thickness 1'),
        ('thickness 2', 'Thickness 2'),
       
    ]
    substrate_thickness = models.CharField(max_length=100, choices=SUBSTRATE_THICKNESS_CHOICES, verbose_name='Substrate Thickness')
    COPPER_THICKNESS_CHOICES = [
        ('copper 1', 'Copper 1'),
        ('copper 2', 'Copper 2'),
        
    ]
    copper_thickness = models.CharField(max_length=100, choices=COPPER_THICKNESS_CHOICES, verbose_name='Copper Thickness')
    SINGLE_DOUBLE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double Side'),
    ]
    single_double_side = models.CharField(max_length=100, choices=SINGLE_DOUBLE_CHOICES, verbose_name='Single/Double Side')
    quantity = models.IntegerField(verbose_name='Quantity', validators=[MinValueValidator(1)])
    length = models.DecimalField(default=0,max_digits=10, decimal_places=2, verbose_name='Length (cm)')
    breadth = models.DecimalField(default=0,max_digits=10, decimal_places=2, verbose_name='Breadth (cm)')
    SURFACE_PAD_FINISH_CHOICES = [
    ('None','None'),
    ('ENIG', 'ENIG'),
    ('HASL', 'HASL'),
    ('PTH', 'PTH'),
    ('Solder', 'Solder'),
    ('Tin coating', 'Tin coating'),
    ('3M tape', '3M tape'),
   
    ]
    surface_pad_finish = models.CharField(max_length=100, choices=SURFACE_PAD_FINISH_CHOICES, verbose_name='Surface Pad Finish', default='ENIG')
    custom_or_default = models.CharField(max_length=20, verbose_name='Custom or Default', default='default')
    payment_status = models.CharField(max_length=20, verbose_name='Payment Status', default='not paid')
    quotation_status = models.CharField(max_length=20, verbose_name='Quotation Status', default='sent')
    def __str__(self):
        return f"Quotation Number: {self.quotation_number}, Name: {self.name}"
    class Meta:
        managed = True
        db_table = 'D_quotation'

@receiver(pre_save, sender=D_quotation)
def set_user(sender, instance, **kwargs):
    # Check if the user field is not already set
    if not instance.user_id:
        instance.user = instance.user 

class Customquotation(models.Model):
    
    user= models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    quotation_number = models.CharField(max_length=20,unique=True,default=QuotationNumberGenerator.generate_quotation_number, editable=False)
    name = models.CharField(max_length=100, validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Name must contain only alphabets and spaces')])
    contact_person = models.CharField(max_length=30, validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Contact person must contain only alphabets and spaces')])
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(regex='^[0-9]*$', message='Phone number must contain only numbers')])
    email = models.EmailField()
    material = models.CharField(max_length=100)
    substrate_thickness = models.FloatField()
    copper_thickness = models.FloatField()
    SINGLE_DOUBLE_CHOICES = [
        ('single', 'Single Side'),
        ('double', 'Double Side'),
    ]
    single_double_side = models.CharField(max_length=10, choices=SINGLE_DOUBLE_CHOICES)
    quantity = models.IntegerField()
    length = models.FloatField()
    breadth = models.FloatField()
    delivery_date = models.DateField()
    description = models.TextField()
    custom_or_default = models.CharField(max_length=20, verbose_name='Custom or Default', default='custom')
    payment_status = models.CharField(max_length=20, verbose_name='Payment Status', default='pending')
    quotation_status = models.CharField(max_length=20, verbose_name='Quotation Status', default='not prepared')


    def __str__(self):
        return f"Quotation Number: {self.quotation_number}, Name: {self.name}"
    class Meta:
        managed = True
        db_table = 'Customquotation'
@receiver(pre_save, sender=Customquotation)
def set_user(sender, instance, **kwargs):
    # Check if the user field is not already set
    if not instance.user_id:
        instance.user = instance.user 



class CustomerDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_detail')
    customer_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    total_orders = models.IntegerField(default=0)
    cancel_orders = models.IntegerField(default=0)
    delivered_orders = models.IntegerField(default=0)

    def __str__(self):
       return self.user.username


