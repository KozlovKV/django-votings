from menu_app.view_subclasses import TemplateViewWithMenu
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
    template_name = 'reports_list.html'

    @staticmethod
    def get_reports_list():
        res = []
        model_list = Reports.objects.filter(status=0)
        for model_note in model_list:
            dict_note = {
                'theme': model_note.theme,
                'object_url': model_note.get_object_url_from_report(),
                'content': model_note.content,
                'author': model_note.author,
                'date': model_note.create_date,
            }
            res.append(dict_note)
        return res

    def get_context_data(self, **kwargs):
        context = super(ReportsListView, self).get_context_data(**kwargs)
        context.update({
            'reports': self.get_reports_list()
        })
        return context


class SendReportView(TemplateViewWithMenu):  # TODO: https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
    template_name = 'send.html'

    def get(self, request, *args, **kwargs):
        """
            Добавление уникального для GET-запроса контекста в self.extra_context
            Логика работы с БД
            Да в общем всё что душе угодно (При ненадобности можно вообще удалить)
        """
        return super(SendReportView, self).get(self, request, *args, **kwargs)
