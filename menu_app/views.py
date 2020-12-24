from django.contrib.auth.views import LoginView
from django.shortcuts import render
import django.contrib.auth.forms as auth_forms


# Create your views here.


def get_menu_context(request):
    menu_context = [
        {'url': '/', 'label': 'Главная'},
        {'url': '/vote/test/', 'label': 'Голосования'},
    ]
    if request.user.is_authenticated:
        menu_context.append({'url': '/report/test/', 'label': 'Поддержка'})
    return menu_context


def get_profile_menu_context(request):
    if request.user.is_authenticated:
        profile_menu_context = [
            {'url': '/profile/test/', 'label': 'Профиль'},
            {'url': '/logout/', 'label': 'Выход'}
        ]
    else:
        form = auth_forms.AuthenticationForm(request)
        profile_menu_context = {
            'login_form': form,
            'usr': form.base_fields['username'],
            'pswd': form.base_fields['password']
        }
    return profile_menu_context


def get_full_menu_context(request):
    context = {
        'menu': get_menu_context(request),
        'profile_menu': get_profile_menu_context(request)
    }
    if not request.user.is_authenticated:
        context['form'] = context['profile_menu']['login_form']
    return context


def index_page(request):
    context = get_full_menu_context(request)
    return render(request, 'index.html', context)


class LoginViewDetailed(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu_context(self.request)
        context['profile_menu'] = get_profile_menu_context(self.request)
        return context
