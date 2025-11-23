from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'company_name',
            'street',
            'house_number',
            'postal_code',
            'city',
            'phone',
            'email',
            'tax_number',
            'bank_details',
        ]
        widgets = {
            'bank_details': forms.Textarea(attrs={'rows': 4}),
        }
