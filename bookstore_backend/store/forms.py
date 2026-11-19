from django import forms

from .models import Order, Subscriber


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']

    def validate_unique(self):
        # Duplicate emails are handled in the view (re-subscribe is not an error).
        pass


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address']
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}
