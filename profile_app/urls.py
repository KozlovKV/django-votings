from django.contrib import admin
from django.urls import path, include

import django_registration.backends.activation.urls as reg_urls
import django.contrib.auth.urls as auth_urls
import menu_app.views as menu

urlpatterns = auth_urls.urlpatterns
urlpatterns[0] = path('login/', menu.LoginViewDetailed.as_view(), name='login')

reg_patterns = reg_urls.urlpatterns
# reg_patterns[2] = path(
#         "register/",
#         menu.RegistrationViewDetailed.as_view(),
#         name="django_registration_register",
#     )

urlpatterns += reg_patterns
