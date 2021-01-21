from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail
from django.utils import timezone

from menu_app.view_menu_context import get_full_site_url
from menu_app.view_subclasses import TemplateViewWithMenu, TemplateEmailSender
from moderation_app.forms import CommentForm, EditRequestForm
from moderation_app.models import Reports, VoteChangeRequest
from moderation_app.view_subclasses import ReportCloseTemplateView
from vote_app.models import Votings


class TestModerView(TemplateViewWithMenu):
    template_name = 'report_test.html'


class ModerationPanelView(TemplateViewWithMenu):
    template_name = 'moderation_main.html'

    def get_context_data(self, **kwargs):
        context = super(ModerationPanelView, self).get_context_data(**kwargs)
        context.update({
            'reports': {
                'all': len(Reports.objects.all()),
                'submitted': len(Reports.objects.filter(status=Reports.SUBMITTED)),
                'rejected': len(Reports.objects.filter(status=Reports.REJECTED)),
                'processed': len(Reports.objects.exclude(status=Reports.IN_PROCESS)),
            },
            'change_request': {
                'all': len(VoteChangeRequest.objects.all()),
            },
        })
        return context


def get_change_requests_list_context():
    res = []
    model_list = VoteChangeRequest.objects.all()
    for model_note in model_list:
        dict_note = {
            'title': model_note.voting.title,
            'date': model_note.date,
            'form_url': reverse('moder_change_request_form', args=(model_note.pk,)),
        }
        res.append(dict_note)
    return res


class ChangeRequestsListView(TemplateViewWithMenu):
    template_name = 'change_requests_list.html'

    def get_context_data(self, **kwargs):
        context = super(ChangeRequestsListView, self).get_context_data(**kwargs)
        context.update({
            'change_requests': get_change_requests_list_context(),
        })
        return context


class ChangeRequestFormView(generic_detail.DetailView, TemplateViewWithMenu):
    template_name = 'change_request_form.html'
    object = None
    model = VoteChangeRequest
    pk_url_kwarg = 'request_id'

    def get_context_data(self, **kwargs):
        context = super(ChangeRequestFormView, self).get_context_data(**kwargs)
        context.update({
            'form': EditRequestForm
        })
        return context


def get_reports_list_context():
    res = []
    model_list = Reports.objects.filter(status=0)
    for model_note in model_list:
        dict_note = {
            'id': model_note.pk,
            'theme': model_note.get_humanity_theme_name(),
            'object_url': model_note.get_object_url_from_report(),
            'content': model_note.content,
            'author': model_note.author,
            'date': model_note.create_date,
            'submit_url': reverse('moder_report_submit', args=(model_note.pk,)),
            'reject_url': reverse('moder_report_reject', args=(model_note.pk,)),
        }
        res.append(dict_note)
    return res


class ReportsListView(TemplateViewWithMenu):
    template_name = 'report/reports_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReportsListView, self).get_context_data(**kwargs)
        context.update({
            'reports': get_reports_list_context()
        })
        return context


class ReportSubmitView(ReportCloseTemplateView):
    template_name = 'report/report_submit.html'
    new_status = 1
    new_status_name = 'Одобрена'


class ReportRejectView(ReportCloseTemplateView):
    template_name = 'report/report_reject.html'
    new_status = 2
    new_status_name = 'Отклонена'


class SendReportView(TemplateViewWithMenu):  # TODO: https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
    template_name = 'send.html'

    def get(self, request, *args, **kwargs):
        """
            Добавление уникального для GET-запроса контекста в self.extra_context
            Логика работы с БД
            Да в общем всё что душе угодно (При ненадобности можно вообще удалить)
        """
        return super(SendReportView, self).get(self, request, *args, **kwargs)