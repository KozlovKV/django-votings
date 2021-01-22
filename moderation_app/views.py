from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail
from django.utils import timezone

from menu_app.view_menu_context import get_full_site_url
from menu_app.view_subclasses import TemplateViewWithMenu, TemplateEmailSender
from moderation_app.forms import CommentForm, EditRequestForm
from moderation_app.models import Reports, VoteChangeRequest
from moderation_app.forms import CommentForm, ModeledReportCreateForm
from moderation_app.models import Reports
from moderation_app.view_subclasses import ReportCloseTemplateView
from vote_app.models import Votings


def get_reports_list_context(model_list):
    res = []
    for model_note in model_list:
        dict_note = {
            'object': model_note,
        }
        res.append(dict_note)
    return res


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


class ReportsListView(TemplateViewWithMenu):
    template_name = 'report/reports_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReportsListView, self).get_context_data(**kwargs)
        context.update({
            'reports': get_reports_list_context(Reports.objects.filter(status=Reports.IN_PROCESS))
        })
        return context


class ReportSubmitView(ReportCloseTemplateView):
    template_name = 'report/report_submit.html'
    new_status = Reports.SUBMITTED
    new_status_name = 'Одобрена'


class ReportRejectView(ReportCloseTemplateView):
    template_name = 'report/report_reject.html'
    new_status = Reports.REJECTED
    new_status_name = 'Отклонена'


class SendReportView(TemplateViewWithMenu, generic_edit.CreateView):  # TODO: https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
    template_name = 'send.html'
    object = None
    model = Reports
    form_class = ModeledReportCreateForm

    def get_context_data(self, **kwargs):
        context = super(SendReportView, self).get_context_data()
        context.update({
            'reports': get_reports_list_context(Reports.objects.filter(author=self.request.user))
        })
        return context

    def post(self, request, *args, **kwargs):
        post_response = super(SendReportView, self).post(self, request, *args, **kwargs)
        return post_response
