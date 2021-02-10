"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

import apps.menu_app.views as menu

import apps.profile_app.views as profile
from settings import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu.IndexView.as_view(), name='menu'),

    path('vote/', include('apps.vote_app.urls')),

    path('profile/view/<int:profile_id>/', profile.ProfilePageView.as_view(), name='profile_view'),

    path('account/', include('apps.profile_app.urls')),

    path('moderation/', include('apps.moderation_app.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
