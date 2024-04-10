from django.contrib import admin
from customer.models import D_quotation,Customquotation,CustomerDetail,Transaction
# Register your models here.
class Cust_entry(admin.ModelAdmin):
    list_displat=['user', 'quotation_number',' name',' contact_person','phone_number','email ','material','substrate_thickness','copper_thickness','single_double_side','quantity','length',' breadth','surface_pad_finish','cost']
class Custm_entry(admin.ModelAdmin):
    list_d=['user',' quotation_number',' name',' contact_person','phone_number','email ','material','substrate_thickness','copper_thickness','single_double_side','quantity','length',' breadth','delivery_date','description','cost']
admin.site.register(D_quotation,Cust_entry)
admin.site.register( Customquotation,Custm_entry)
admin.site.register( CustomerDetail)
admin.site.register(Transaction)