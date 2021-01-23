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

import menu_app.views as menu
import vote_app.views as vote
import profile_app.views as profile
import moderation_app.views as moder
import moderation_app.view_report_subclasses as report
import moderation_app.view_request_subclasses as change_request
from django_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu.IndexView.as_view(), name='menu'),

    path('vote/test/', vote.test_page),
    path('vote/list/', vote.VoteListPageView.as_view(), name='vote_list'),
    path('vote/create/', vote.CreateVotingView.as_view(), name='vote_create'),
    path('vote/edit/<int:voting_id>/', vote.EditVotingView.as_view(), name='vote_edit'),
    path('vote/delete/<int:voting_id>/', vote.DeleteVotingView.as_view(), name='vote_delete'),
    path('vote/view/<int:voting_id>/', vote.VotingView.as_view(), name='vote_view'),

    path('profile/view/<int:profile_id>/', profile.ProfilePageView.as_view(), name='profile_view'),

    path('account/', include('profile_app.urls')),

    path('moderation/send/', report.SendReportView.as_view(), name='moder_report_send'),
    path('moderation/send/success/', report.SendReportSuccessView.as_view(), name='moder_report_send_success'),
    path('moderation/manage/', moder.ModerationPanelView.as_view(), name='moder_manage'),
    path('moderation/manage/reports/list/', report.ReportsListView.as_view(), name='moder_reports_list'),
    path('moderation/manage/reports/submit/<int:report_id>/', report.ReportSubmitView.as_view(),
         name='moder_report_submit'),
    path('moderation/manage/reports/reject/<int:report_id>/', report.ReportRejectView.as_view(),
         name='moder_report_reject'),
    path('moderation/manage/change_request/list/', change_request.ChangeRequestsListView.as_view(),
         name='moder_change_request_list'),
    path('moderation/manage/change_request/<int:request_id>/', change_request.ChangeRequestView.as_view(),
         name='moder_change_request_form'),
    path('moderation/manage/change_request/submit/<int:request_id>/', change_request.ChangeRequestSubmitView.as_view(),
         name='moder_change_request_submit'),
    path('moderation/manage/change_request/reject/<int:request_id>/', change_request.ChangeRequestRejectView.as_view(),
         name='moder_change_request_reject'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
