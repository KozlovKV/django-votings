from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

import profile_app.forms as profile_forms
from profile_app.models import AdditionUserInfo


def get_menu_context(request):
    menu_context = [
        {'url': reverse('menu'), 'label': 'Главная'},
        {'url': reverse('vote_list'), 'label': 'Голосования'},
    ]
    if request.user.is_authenticated:
        menu_context.append({'url': reverse('moder_report_send'), 'label': 'Поддержка'})
    return menu_context


def get_profile_menu_context(request):
    profile_menu_context = []
    if request.user.is_authenticated:
        profile_menu_context = [
            {'url': reverse('profile_view', args=(request.user.id,)), 'label': request.user},
            {'url': reverse('logout'), 'label': 'Выход'}
        ]
    return profile_menu_context


def get_full_site_url(request):
    scheme = 'http://' if not request.is_secure() else 'https://'
    return scheme + str(get_current_site(request))


def get_full_menu_context(request):
    context = {
        'menu': get_menu_context(request),
        'profile_menu': get_profile_menu_context(request),
        'rights': 0,
        'status': 'Обычный',
    }
    if not request.user.is_authenticated:
        context['login_form'] = profile_forms.ModifiedAuthenticationForm(request.POST)
        context['reg_form'] = profile_forms.ModifiedRegistrationForm(request.POST)
    else:
        info = AdditionUserInfo.objects.get(user=request.user)
        context['rights'] = info.user_rights
        context['right_name'] = info.get_right_name()
        if info.user_rights == 2:
            context['profile_menu'].append({'url': '/admin', 'label': 'Админ'})
    context['reset_form'] = profile_forms.ModifiedPasswordResetForm(request.POST)
    context['main_url'] = get_full_site_url(request)
    return context
