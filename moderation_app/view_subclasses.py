from django.urls import reverse_lazy
import django.views.generic.edit as generic_edit
from django.utils import timezone

from menu_app.view_menu_context import get_full_site_url
from menu_app.view_subclasses import TemplateViewWithMenu, TemplateEmailSender
from moderation_app.forms import CommentForm
from moderation_app.models import Reports


class ReportCloseTemplateView(TemplateViewWithMenu, generic_edit.FormView):
    template_name = 'report/report_reject.html'
    form_class = CommentForm
    success_url = reverse_lazy('moder_manage')
    new_status = 2
    new_status_name = 'Отклонена'

    def get_email_context(self):
        report_id = self.kwargs['report_id']
        report = Reports.objects.get(pk=report_id)
        context = {
            'report_id': report_id,
            'status': self.new_status_name,
            'comment': self.request.POST.get('comment', ''),
            'moder': self.request.user,
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
