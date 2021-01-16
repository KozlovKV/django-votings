from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit

from menu_app.view_subclasses import TemplateViewWithMenu
from moderation_app.forms import CommentForm
from moderation_app.models import Reports


class TestModerView(TemplateViewWithMenu):
    template_name = 'report_test.html'


class ModerationPanelView(TemplateViewWithMenu):
    template_name = 'moderation_main.html'

    def get_context_data(self, **kwargs):
        context = super(ModerationPanelView, self).get_context_data(**kwargs)
        context.update({
            'reports': {
                'all': len(Reports.objects.all()),
                'submitted': len(Reports.objects.filter(status=1)),
                'rejected': len(Reports.objects.filter(status=2)),
                'processed': len(Reports.objects.exclude(status=0)),
            },
            'change_request': {
                'all': len(Reports.objects.all()),
                'submitted': len(Reports.objects.filter(status=1)),
                'rejected': len(Reports.objects.filter(status=2)),
                'processed': len(Reports.objects.exclude(status=0)),
            },
        })
        return context


class ChangeRequestsListView(TemplateViewWithMenu):
    template_name = 'change_requests_list.html'


class ChangeRequestFormView(TemplateViewWithMenu):
    template_name = 'change_request_form.html'

    def get(self, request, *args, **kwargs):
        self.extra_context = kwargs
        return super(ChangeRequestFormView, self).get(self, request, *args, **kwargs)


class ReportsListView(TemplateViewWithMenu):
    template_name = 'report/reports_list.html'

    @staticmethod
    def get_reports_list():
        res = []
        model_list = Reports.objects.filter(status=0)
        for model_note in model_list:
            dict_note = {
                'id': model_note.id,
                'theme': model_note.theme,
                'object_url': model_note.get_object_url_from_report(),
                'content': model_note.content,
                'author': model_note.author,
                'date': model_note.create_date,
                'submit_url': reverse('moder_report_submit', args=(model_note.id,)),
                'reject_url': reverse('moder_report_reject', args=(model_note.id,)),
            }
            res.append(dict_note)
        return res

    def get_context_data(self, **kwargs):
        context = super(ReportsListView, self).get_context_data(**kwargs)
        context.update({
            'reports': self.get_reports_list()
        })
        return context


class ReportSubmitView(TemplateViewWithMenu, generic_edit.FormView):
    template_name = 'report/report_submit.html'
    form_class = CommentForm
    success_url = reverse_lazy('moder_manage')
    # email_subject_template = 'report/email_subject.txt'
    # email_body_template = 'report/email_body.txt'

    def get_email_context(self):
        report_id = self.kwargs['report_id']
        report = Reports.objects.get(pk=report_id)
        context = {
            'status': 'Одобрена',
            'comment': self.form_class.comment,
            'moder': self.extra_context['user'],
            'date': report.close_date
        }

    # def form_valid(self, form):
    #     super(ReportSubmitView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        post_resp = super(ReportSubmitView, self).post(self, request, *args, **kwargs)
        print(post_resp)




class SendReportView(TemplateViewWithMenu):  # TODO: https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
    template_name = 'send.html'

    def get(self, request, *args, **kwargs):
        """
            Добавление уникального для GET-запроса контекста в self.extra_context
            Логика работы с БД
            Да в общем всё что душе угодно (При ненадобности можно вообще удалить)
        """
        return super(SendReportView, self).get(self, request, *args, **kwargs)
