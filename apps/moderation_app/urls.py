from django.urls import path

from apps.moderation_app import views as moder_main
from apps.moderation_app import view_request_subclasses as change_request
from apps.moderation_app import view_report_subclasses as report

urlpatterns = [
    path('send/', report.SendReportView.as_view(), name='moder_report_send'),
    path('send/success/', report.SendReportSuccessView.as_view(), name='moder_report_send_success'),
    path('manage/', moder_main.ModerationPanelView.as_view(), name='moder_manage'),
    path('manage/reports/list/', report.ReportsListView.as_view(), name='moder_reports_list'),
    path('manage/reports/submit/<int:report_id>/', report.ReportSubmitView.as_view(),
         name='moder_report_submit'),
    path('manage/reports/reject/<int:report_id>/', report.ReportRejectView.as_view(),
         name='moder_report_reject'),
    path('manage/change_request/list/', change_request.ChangeRequestsListView.as_view(),
         name='moder_change_request_list'),
    path('manage/change_request/<int:request_id>/', change_request.ChangeRequestView.as_view(),
         name='moder_change_request_form'),
    path('manage/change_request/submit/<int:request_id>/', change_request.ChangeRequestSubmitView.as_view(),
         name='moder_change_request_submit'),
    path('manage/change_request/reject/<int:request_id>/', change_request.ChangeRequestRejectView.as_view(),
         name='moder_change_request_reject'),
]