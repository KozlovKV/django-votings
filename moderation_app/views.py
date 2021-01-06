from menu_app.view_subclasses import TemplateViewWithMenu


class TestModerView(TemplateViewWithMenu):
    template_name = 'report_test.html'


class SendReportView(TemplateViewWithMenu):  # TODO: https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
    template_name = 'send.html'

