from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from menu_app.views import get_full_menu_context


def test_page(request):
    context = get_full_menu_context(request)
    return render(request, 'profile_test.html', context)


def view_profile(request, profile_id):
    context = {
        'profile_id': profile_id,
        'profile_user': User.objects.get(pk=profile_id) if profile_id != 0 else request.user
    }
    context.update(get_full_menu_context(request))
    return render(request, 'profile_page.html', context)
