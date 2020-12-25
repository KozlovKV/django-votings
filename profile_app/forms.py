import django_registration.forms as reg_forms
from django import forms


class ModifiedRegistrationForm(reg_forms.RegistrationFormUniqueEmail):
    username = reg_forms.RegistrationFormUniqueEmail.base_fields['username']
