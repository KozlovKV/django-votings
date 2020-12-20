from django.shortcuts import render

# Create your views here.
from menu_app.views import get_full_menu_context


def test_page(request):
    context = get_full_menu_context(request)
    return render(request, 'report_test.html', context)
