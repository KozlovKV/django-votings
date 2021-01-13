from menu_app.view_subclasses import TemplateViewWithMenu


class TestModerView(TemplateViewWithMenu):
    template_name = 'report_test.html'


class ModerationPanelView(TemplateViewWithMenu):
    template_name = 'moderation_main.html'


class ChangeRequestsListView(TemplateViewWithMenu):
    template_name = 'change_requests_list.html'


class ReportsListView(TemplateViewWithMenu):
    template_name = 'reports_list.html'


class SendReportView(TemplateViewWithMenu):  # TODO: https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
    template_name = 'send.html'

    def get(self, request, *args, **kwargs):
        """
            Добавление уникального для GET-запроса контекста в self.extra_context
            Логика работы с БД
            Да в общем всё что душе угодно (При ненадобности можно вообще удалить)
        """
        return super(SendReportView, self).get(self, request, *args, **kwargs)

