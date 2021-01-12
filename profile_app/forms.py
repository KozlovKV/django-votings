from django import forms
import django_registration.forms as reg_forms
import django.contrib.auth.forms as auth_forms
from django.contrib.auth import password_validation


class ModifiedAuthenticationForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Логин',
            'class': 'input',
        }
    ))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Пароль',
            'class': 'input',
        }),
    )


class ModifiedRegistrationForm(reg_forms.RegistrationFormUniqueEmail):
    username = auth_forms.UsernameField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Логин',
            'class': 'input',
        }))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Электронная почта',
            'class': 'input',
        }))
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Пароль',
            'class': 'input',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Подтвердите пароль',
            'class': 'input',
        }),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )


class ModifiedPasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label='Электронная почта',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'Электронная почта',
            'class': 'input wide',
        })
    )


class ModifiedSetPasswordForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Новый пароль',
            'class': 'input wide',
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Подтвердите пароль',
            'class': 'input wide',
        }),
    )
