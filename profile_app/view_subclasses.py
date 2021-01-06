from abc import ABC
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import LoginView
import django_registration.backends.activation.views as reg_act_views

import profile_app.forms as profile_forms
from menu_app.view_subclasses import TemplateViewWithMenu
from menu_app.views import get_full_menu_context


class LoginViewDetailed(LoginView, TemplateViewWithMenu):
    form_class = profile_forms.ModifiedAuthenticationForm


class RegistrationViewDetailed(reg_act_views.RegistrationView, TemplateViewWithMenu):
    form_class = profile_forms.ModifiedRegistrationForm
    success_url = reverse_lazy('django_registration_complete')


class ActivationViewDetailed(reg_act_views.ActivationView, TemplateViewWithMenu):
    pass
