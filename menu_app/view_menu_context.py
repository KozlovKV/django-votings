import profile_app.forms as profile_forms


def get_menu_context(request):
    menu_context = [
        {'url': '/', 'label': 'Главная'},
        {'url': '/vote/list/', 'label': 'Голосования'},
    ]
    if request.user.is_authenticated:
        menu_context.append({'url': '/moderation/send/', 'label': 'Поддержка'})
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
    context['reset_form'] = profile_forms.ModifiedPasswordResetForm(request.POST)
    return context
