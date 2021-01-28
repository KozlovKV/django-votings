from django.contrib.auth import views
from django.urls import path

import profile_app.view_subclasses as reg_subclasses
import menu_app.view_subclasses as menu_subclasses


urlpatterns = [
    path('login/', reg_subclasses.LoginViewDetailed.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', reg_subclasses.PasswordResetViewDetailed.as_view(), name='password_reset'),
    path('password_reset/done/', menu_subclasses.TemplateViewWithMenu.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', reg_subclasses.PasswordResetConfirmViewDetailed.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', menu_subclasses.TemplateViewWithMenu.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

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
