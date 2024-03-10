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
from customer import views
from django.contrib.auth.views import LogoutView
from .views import Customer_entry1,user_login,register,home,place_order,your_order,customized_quotation
urlpatterns = [
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    #path('login/',views.login),
    #path('staff_details/',views.staff_details,name='staff_details'),
    #path('add_staff/',views.add_staff,name='add_staff'),
    path('create-user/', Customer_entry1.as_view(), name='Customer_entry'),
    path('customer_entry/', views.display_customer_entries, name='customer_entry'),
    path('customized_quotation/', customized_quotation.as_view(), name='customized_quotation'),
    #path('customer_registration/',views.Customer_registration , name='customer_registration'),
    path('register/', register, name='register'),
    path('place_order/', place_order, name='place_order'),
    path('your_order/', your_order, name='your_order'),

]
