from django import forms

class Custom_quotation(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'pattern': '[A-Za-z ]+', 'title': 'Alphabets only'}))
    contact_person = forms.CharField(label='Contact Person', max_length=30, widget=forms.TextInput(attrs={'pattern': '[A-Za-z ]+', 'title': 'Alphabets only'}))
    phone_number = forms.CharField(label='Phone Number', max_length=10, widget=forms.TextInput(attrs={'pattern': '[0-9]+', 'title': 'Numbers only'}))
    email = forms.EmailField(label='Email')
    material = forms.CharField(label='Material', max_length=100)
    substrate_thickness = forms.FloatField(label='Substrate Thickness (mm)')
    copper_thickness = forms.FloatField(label='Copper Thickness(mm)')
    SINGLE_DOUBLE_CHOICES = [
        ('single', 'Single Side'),
        ('double', 'Double Side'),
    ]
    single_double_side = forms.ChoiceField(label='Single/Double Side', choices=SINGLE_DOUBLE_CHOICES)
    quantity = forms.IntegerField(label='Quantity')
    length = forms.FloatField(label='Length cm')
    breadth = forms.FloatField(label='Breadth cm')
    delivery_date=forms.DateField(label='Delivery Date', widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(label='Description', widget=forms.Textarea)
