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
from django.urls import path, include

import menu_app.views as menu
import vote_app.views as vote
import profile_app.views as profile
import moderation_app.views as report


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu.IndexView.as_view()),

    path('vote/test/', vote.test_page),
    # path('vote/create/', vote.vote_create_page),
    path('vote/create/', vote.vote_create_page_alt),
    path('vote/edit/<int:voting_id>/', vote.vote_edit_page),
    path('listOfVotes/', vote.list_of_votes),

    path('profile/test/', profile.TestProfileView.as_view()),
    path('profile/view/<int:profile_id>/', profile.ProfilePageView.as_view()),

    path('moderation/test/', report.TestModerView.as_view()),
    path('moderation/manage/', report.TestModerView.as_view()),
    path('moderation/send/', report.SendReportView.as_view()),

    path('account/', include('profile_app.urls')),
]
