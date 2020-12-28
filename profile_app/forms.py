from django import forms
import django_registration.forms as reg_forms
import django.contrib.auth.forms as auth_forms
from django.contrib.auth import password_validation


class ModifiedAuthenticationForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Пароль'
        }),
    )


class ModifiedRegistrationForm(reg_forms.RegistrationFormUniqueEmail):
    username = auth_forms.UsernameField(widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Электронная почта'}))
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Пароль',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Подтвердите пароль',
        }),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
