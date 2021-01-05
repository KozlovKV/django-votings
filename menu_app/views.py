from abc import ABC

from django.contrib.auth.views import LoginView
from django.shortcuts import render
import django.contrib.auth.forms as auth_forms
import django_registration.forms as reg_forms

from django_registration.views import RegistrationView
# from menu_app.forms import AuthWithPlHolders
import profile_app.forms as profile_forms


def get_menu_context(request):
    menu_context = [
        {'url': '/', 'label': 'Главная'},
        {'url': '/vote/test/', 'label': 'Голосования'},
    ]
    if request.user.is_authenticated:
        menu_context.append({'url': '/moderation/send/', 'label': 'Поддержка'})
    # else:
    #     menu_context.append({'url': '/account/register', 'label': 'Регистрация'})
    return menu_context


def get_profile_menu_context(request):
    profile_menu_context = []
    if request.user.is_authenticated:
        profile_menu_context = [
            {'url': '/profile/view/0/', 'label': request.user},
            {'url': '/account/logout/', 'label': 'Выход'}
        ]
    return profile_menu_context


def get_full_menu_context(request):
    context = {
        'menu': get_menu_context(request),
        'profile_menu': get_profile_menu_context(request)
    }
    if not request.user.is_authenticated:
        context['login_form'] = profile_forms.ModifiedAuthenticationForm(request.POST)
        context['reg_form'] = profile_forms.ModifiedRegistrationForm(request.POST)
        # context['reg_form'] = reg_forms.RegistrationFormUniqueEmail(request.POST)
    return context


def index_page(request):
    context = get_full_menu_context(request)
    return render(request, 'index.html', context)


class LoginViewDetailed(LoginView):
    form_class = profile_forms.ModifiedAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu_context(self.request)
        context['profile_menu'] = get_profile_menu_context(self.request)
        context['login_form'] = profile_forms.ModifiedAuthenticationForm(self.request.POST)
        context['reg_form'] = profile_forms.ModifiedRegistrationForm(self.request.POST)
        # context['reg_form'] = reg_forms.RegistrationFormUniqueEmail(self.request.POST)
        return context


class RegistrationViewDetailed(RegistrationView, ABC):
    form_class = profile_forms.ModifiedRegistrationForm
    # form_class = reg_forms.RegistrationFormUniqueEmail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu_context(self.request)
        context['profile_menu'] = get_profile_menu_context(self.request)
        context['login_form'] = profile_forms.ModifiedAuthenticationForm(self.request.POST)
        context['reg_form'] = profile_forms.ModifiedRegistrationForm(self.request.POST)
        # context['reg_form'] = reg_forms.RegistrationFormUniqueEmail(self.request.POST)
        return context
