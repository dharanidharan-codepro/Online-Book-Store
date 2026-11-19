from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='We will send order receipts and confirmations here.'
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Choose a unique username',
            'autocomplete': 'username',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'you@example.com',
            'autocomplete': 'email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Create a secure password',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
        })


class StaffAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        user = self.get_user()
        if user is not None and not user.is_staff:
            raise forms.ValidationError('This account does not have staff access.')
        return cleaned_data
