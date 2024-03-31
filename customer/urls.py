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
from django.contrib.auth import views as auth_views
from .views import Customer_entry1,user_login,register,home,place_order,your_order,customized_quotation,forgot_password_view,password_reset_confirm_view
urlpatterns = [
    path('login/', user_login, name='users_login'),
    path('home/', home, name='home'),
    # path('customer_detail/', views.company_detail, name='company_detail'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('user_logout/',LogoutView.as_view(next_page='users_login'),name='user_logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('create-user/', Customer_entry1.as_view(), name='Defalut'),
    path('customer_entry/', views.display_customer_entries, name='customer_entry'),
    path('customized_quotation/', customized_quotation.as_view(), name='customized_quotation'),
    path('register/', register, name='register'),
    path('place_order/', place_order.as_view(), name='place_order'),
    path('your_order/', your_order, name='your_order'),

]
