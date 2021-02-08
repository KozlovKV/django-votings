from django.urls import reverse_lazy

import django.contrib.auth.views as auth_views
import django_registration.backends.activation.views as reg_act_views
from apps.menu_app.view_subclasses import TemplateViewWithMenu

import profile_app.forms as profile_forms

import profile_app.models as profile_models


class LoginViewDetailed(auth_views.LoginView, TemplateViewWithMenu):
    form_class = profile_forms.ModifiedAuthenticationForm


class RegistrationViewDetailed(reg_act_views.RegistrationView, TemplateViewWithMenu):
    form_class = profile_forms.ModifiedRegistrationForm
    success_url = reverse_lazy('django_registration_complete')

    def register(self, form):
        new_user = super(RegistrationViewDetailed, self).register(form)
        additional_info = profile_models.AdditionUserInfo(user=new_user)
        additional_info.save()
        return new_user


class ActivationViewDetailed(reg_act_views.ActivationView, TemplateViewWithMenu):
    pass


class PasswordResetViewDetailed(auth_views.PasswordResetView, TemplateViewWithMenu):
    form_class = profile_forms.ModifiedPasswordResetForm


class PasswordResetConfirmViewDetailed(auth_views.PasswordResetConfirmView, TemplateViewWithMenu):
    form_class = profile_forms.ModifiedSetPasswordForm
