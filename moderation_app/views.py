from menu_app.view_subclasses import TemplateViewWithMenu
from moderation_app.models import Reports, VoteChangeRequest


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
