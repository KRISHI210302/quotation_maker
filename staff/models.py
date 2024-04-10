from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomCreation(models.Model):
    quotation_number = models.CharField(max_length=100, unique=True)
    material_charge = models.DecimalField(max_digits=10, decimal_places=2)  # Renamed field
    substrate_thickness = models.DecimalField(max_digits=10, decimal_places=2)
    copper_thickness = models.DecimalField(max_digits=10, decimal_places=2)
    setup_charges = models.DecimalField(max_digits=10, decimal_places=2)
    extra_charges = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Added new field
    quantity = models.IntegerField()  # Added new field
    length = models.DecimalField(max_digits=10, decimal_places=2)  # Added new field
    breadth = models.DecimalField(max_digits=10, decimal_places=2)  # Added new field

    # Added method to calculate total charges
    def calculate_total_charge(self):
        return (
            self.material_charge + self.setup_charges + self.extra_charges +
            self.shipping_charges  # Include shipping charges in total
        )

    total_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Added new field with default

    def save(self, *args, **kwargs):
        # Calculate and update total charge before saving
        self.total_charge = self.calculate_total_charge()* self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return self.quotation_number
class Staffs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

def create_staff_with_user(username, name, designation, email, phone_number, password):
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

    return staff
