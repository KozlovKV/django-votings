from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
from django.utils import timezone

from menu_app.view_menu_context import get_full_site_url
from menu_app.view_subclasses import TemplateViewWithMenu, TemplateEmailSender
from moderation_app.forms import CommentForm, ModeledReportCreateForm
from moderation_app.models import Reports
from moderation_app.view_subclasses import ReportCloseTemplateView


class TestModerView(TemplateViewWithMenu):
    template_name = 'report_test.html'


class ModerationPanelView(TemplateViewWithMenu):
    template_name = 'moderation_main.html'

    def get_context_data(self, **kwargs):
        context = super(ModerationPanelView, self).get_context_data(**kwargs)
        context.update({
            'reports': {
                'all': len(Reports.objects.all()),
                'submitted': len(Reports.objects.filter(Status=1)),
                'rejected': len(Reports.objects.filter(Status=2)),
                'processed': len(Reports.objects.exclude(Status=0)),
            },
            'change_request': {
                'all': len(Reports.objects.all()),
                'submitted': len(Reports.objects.filter(Status=1)),
                'rejected': len(Reports.objects.filter(Status=2)),
                'processed': len(Reports.objects.exclude(Status=0)),
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
        model_list = Reports.objects.filter(Status=0)
        for model_note in model_list:
            dict_note = {
                'id': model_note.id,
                'theme': model_note.get_humanity_theme_name(),
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


class ReportSubmitView(ReportCloseTemplateView):
    template_name = 'report/report_submit.html'
    new_status = 1
    new_status_name = 'Одобрена'


class ReportRejectView(ReportCloseTemplateView):
    template_name = 'report/report_reject.html'
    new_status = 2
    new_status_name = 'Отклонена'


class SendReportView(TemplateViewWithMenu, generic_edit.CreateView):  # TODO: https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
    template_name = 'send.html'
    object = None
    model = Reports
    form_class = ModeledReportCreateForm

    def get(self, request, *args, **kwargs):
        """
            Добавление уникального для GET-запроса контекста в self.extra_context
            Логика работы с БД
            Да в общем всё что душе угодно (При ненадобности можно вообще удалить)
        """
        return super(SendReportView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post_response = super(SendReportView, self).post(self, request, *args, **kwargs)

        # TODO: Добавить сохранение вариантов голосования

        # Записать ID новой жалобы для переадресации
        # report_id = self.object.id
        # post_response.url = reverse_lazy('vote_view', args=(report_id,))
        return post_response
