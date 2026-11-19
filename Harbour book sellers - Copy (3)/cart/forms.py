from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'e.g. Dharanidharan'}),
            'email': forms.EmailInput(attrs={'class': 'auth-input', 'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': '+91 98765 43210'}),
            'address': forms.Textarea(attrs={'class': 'auth-input', 'rows': 3, 'placeholder': 'Complete street address, city, state, pincode'}),
        }
        labels = {
            'full_name': 'Full name',
            'email': 'Email address',
            'phone': 'Phone number',
            'address': 'Delivery address',
        }
