from django import forms
import django_registration.forms as reg_forms
import django.contrib.auth.forms as auth_forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
import pytz


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'wide input',
                'placeholder': 'Новое имя',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'wide input',
                'placeholder': 'Новая фамилия',
            }),
        }


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


def get_tz_enum(country=None):
    if country is None:
        return [(tz, tz) for tz in pytz.common_timezones]
    else:
        return [(tz, tz) for tz in pytz.country_timezones(country)]


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
    timezone = forms.ChoiceField(
        label='Часовой пояс',
        choices=get_tz_enum('ru'),
        widget=forms.Select(attrs={
            'class': 'input wide',
        })
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
