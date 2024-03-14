from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
'''
class User(AbstractUser):
    registered_app = models.CharField(max_length=100)

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registered_app = models.CharField(max_length=100) 
    def __str__(self):
        return f"Name: {self.user}"
@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
      if instance.registered_app == 'staff':
            StaffProfile.objects.create(user=instance)
      elif instance.registered_app == 'customer':
            UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_staff_profile(sender, instance, **kwargs):
    try:
          if instance.staffprofile:
            instance.staffprofile.save()# Use lowercase 'staffprofile' instead of 'StaffProfile'
    except StaffProfile.DoesNotExist:
         pass
'''
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
