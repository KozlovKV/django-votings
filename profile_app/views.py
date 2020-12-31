from django.shortcuts import render

# Create your views here.
from menu_app.views import get_full_menu_context


def test_page(request):
    context = get_full_menu_context(request)
    return render(request, 'profile_test.html', context)


def view_own_profile(request):
    context = {}
    context.update(get_full_menu_context(request))
    return render(request, 'profile_page.html', context)
