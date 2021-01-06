from django.urls import path

import django_registration.backends.activation.urls as reg_urls
import django.contrib.auth.urls as auth_urls

import django_registration.backends.activation.views as reg_act_views
import profile_app.view_subclasses as reg_subclasses
import menu_app.view_subclasses as menu_subclasses


urlpatterns = auth_urls.urlpatterns
urlpatterns[0] = path('login/', reg_subclasses.LoginViewDetailed.as_view(), name='login')

reg_patterns = [
    path(
        "activate/complete/",
        menu_subclasses.TemplateViewWithMenu.as_view(
            template_name="django_registration/activation_complete.html",
        ),
        name="django_registration_activation_complete",
    ),
    path(
        "activate/<str:activation_key>/",
        reg_subclasses.ActivationViewDetailed.as_view(),
        name="django_registration_activate",
    ),
    path(
        "register/",
        reg_subclasses.RegistrationViewDetailed.as_view(),
        name="django_registration_register",
    ),
    path(
        "register/complete/",
        menu_subclasses.TemplateViewWithMenu.as_view(
            template_name="django_registration/registration_complete.html",
        ),
        name="django_registration_complete",
    ),
    path(
        "register/closed/",
        menu_subclasses.TemplateViewWithMenu.as_view(
            template_name="django_registration/registration_closed.html",
        ),
        name="django_registration_disallowed",
    ),
]

urlpatterns += reg_patterns
