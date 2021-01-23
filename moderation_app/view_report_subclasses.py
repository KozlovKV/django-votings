from django.urls import reverse_lazy
import django.views.generic.edit as generic_edit
from django.utils import timezone

from menu_app.view_menu_context import get_full_site_url
from menu_app.view_subclasses import TemplateViewWithMenu, TemplateEmailSender
from moderation_app.forms import CommentForm, ModeledReportCreateForm
from moderation_app.models import Reports
from profile_app.models import AdditionUserInfo


def get_reports_list_context(model_list):
    res = []
    for model_note in model_list:
        dict_note = {
            'object': model_note,
        }
        res.append(dict_note)
    return res


class ReportCloseTemplateView(TemplateViewWithMenu, generic_edit.FormView):
    template_name = 'report/report_reject.html'
    form_class = CommentForm
    success_url = reverse_lazy('moder_manage')
    new_status = 2
    new_status_name = 'отклонена'

    def get_email_context(self):
        report_id = self.kwargs['report_id']
        report = Reports.objects.get(pk=report_id)
        context = {
            'report_id': report_id,
            'status': self.new_status_name,
            'comment': self.request.POST.get('comment', ''),
            'moder': self.request.user,
            'right_name': AdditionUserInfo.objects.get(user=self.request.user).get_right_name(),
            'author': report.author,
            'theme': report.get_humanity_theme_name(),
            'main_url': get_full_site_url(self.request),
            'date': report.close_date,
        }
        return context

    def send_close_email(self):
        report_id = self.kwargs['report_id']
        report = Reports.objects.get(pk=report_id)

        email = TemplateEmailSender(to=[report.author.email])
        email.subject_template = 'report/email_subject.txt'
        email.body_template = 'report/email_body.txt'
        email.context = self.get_email_context()
        email.request = self.request
        email.send()

    def save_closed_report(self):
        report_id = self.kwargs['report_id']
        report = Reports.objects.get(pk=report_id)
        report.close_date = timezone.now()
        report.status = self.new_status
        report.save()

    def post(self, request, *args, **kwargs):
        post_resp = super(ReportCloseTemplateView, self).post(self, request, *args, **kwargs)
        self.save_closed_report()
        self.send_close_email()
        return post_resp


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
    new_status_name = 'одобрена'


class ReportRejectView(ReportCloseTemplateView):
    template_name = 'report/report_reject.html'
    new_status = Reports.REJECTED
    new_status_name = 'отклонена'


class SendReportView(TemplateViewWithMenu, generic_edit.CreateView):  # TODO: https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
    template_name = 'send.html'
    object = None
    model = Reports
    form_class = ModeledReportCreateForm

    def get_context_data(self, **kwargs):
        context = super(SendReportView, self).get_context_data()
        reports_list = get_reports_list_context(Reports.objects.filter(author=self.request.user))
        reports_list.reverse()
        context.update({
            'reports': reports_list,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'theme': request.GET.get('theme', None),
            'element': request.GET.get('element', None),
        }
        if self.extra_context['theme'] != str(Reports.VOTING_REPORT):
            self.extra_context['element'] = None
        get_response = super(SendReportView, self).get(request, *args, **kwargs)
        return get_response

    def post(self, request, *args, **kwargs):
        post_response = super(SendReportView, self).post(self, request, *args, **kwargs)
        return post_response


class SendReportSuccessView(TemplateViewWithMenu):
    template_name = 'report_success'
