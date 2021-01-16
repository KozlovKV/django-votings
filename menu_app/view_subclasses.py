from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView, View

from menu_app.view_menu_context import get_full_menu_context


class TemplateViewWithMenu(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_full_menu_context(self.request))
        return context


class TemplateEmailSender(EmailMessage):
    subject_template = ''
    body_template = ''
    context = {}
    request = None

    def send(self, fail_silently=False):
        self.update_from_templates()
        super(TemplateEmailSender, self).send(fail_silently)

    def update_from_templates(self):
        self.subject = render_to_string(
            template_name=self.subject_template,
            context=self.context,
            request=self.request,
        )
        self.subject = "".join(self.subject.splitlines())
        self.body = render_to_string(
            template_name=self.body_template,
            context=self.context,
            request=self.request
        )
