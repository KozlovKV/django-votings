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
        profile_menu_context = {
            'login_form': auth_forms.AuthenticationForm,
        }
    return profile_menu_context


def index_page(request):
    context = {
        'menu': get_menu_context(request),
        'profile_menu': get_profile_menu_context(request)
    }
    return render(request, 'index.html', context)
