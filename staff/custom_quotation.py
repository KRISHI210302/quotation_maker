# forms.py
from django import forms

class Custom_create(forms.Form):
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)
        super(Custom_create, self).__init__(*args, **kwargs)
        for i in range(extra_fields):
            self.fields[f'extra_field_{i}'] = forms.CharField()