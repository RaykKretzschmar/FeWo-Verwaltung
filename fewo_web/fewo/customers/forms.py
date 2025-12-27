from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "customer_type",
            "is_custom_salutation",
            "title",
            "salutation",
            "custom_salutation",
            "first_name",
            "last_name",
            "company_name",
            "city",
            "postal_code",
            "street",
            "house_number",
        ]
        widgets = {
            "customer_type": forms.Select(attrs={"class": "form-control"}),
            "salutation": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "is_custom_salutation": forms.CheckboxInput(attrs={"class": "form-checkbox", "id": "id_is_custom_salutation"}),
            "custom_salutation": forms.TextInput(attrs={"class": "form-control", "id": "id_custom_salutation"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "street": forms.TextInput(attrs={"class": "form-control"}),
            "house_number": forms.TextInput(attrs={"class": "form-control"}),
        }
