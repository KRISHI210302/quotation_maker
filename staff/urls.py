"""quotations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.urls import path, include
from staff import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import  custom_orders

urlpatterns = [
 path('customer_details/',views.customer_details,name='customer_details'),
  path('staff_customer_details/',views.staff_customer_details,name='s_customer_details'),
 path('add_staff/',views.add_staff,name='add_staff'),
  path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',views.password_reset_confirm_view, name='password_reset_confirm'),
 path('staff_login/',views.staff_login,name='staff_login'),
    path('staff_logout/',LogoutView.as_view(next_page='staff_login'),name='staff_logout'),
  path('staff_details/',views.staff_details,name='staff_detail'),
  path('orders/',views.Order_details,name='orders'),
   path('staff_orders/',views.staff_Order_details,name='s_orders'),
  path('custom_orders/',custom_orders,name='custom_orders'),
  path('staff_custom_orders/',views.staff_custom_orders,name='s_custom_orders'),
   path('home/',views.Home,name='home'),
   path('staff_home/',views.staff_home,name='staff_home'),
    path('custom_quotation/<int:entry_id>/',views.custom_create,name='custom'),
    path('staff_custom_quotation/<int:entry_id>/',views.staff_custom_create,name='s_custom'),
     path('upload/',views.upload_excel, name='upload_excel'),


]








