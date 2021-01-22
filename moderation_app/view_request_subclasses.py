from django.urls import reverse
import django.views.generic.detail as generic_detail

from menu_app.view_subclasses import TemplateViewWithMenu
from moderation_app.forms import EditRequestForm
from moderation_app.models import VoteChangeRequest


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
    template_name = 'change_requests/change_requests_list.html'

    def get_context_data(self, **kwargs):
        context = super(ChangeRequestsListView, self).get_context_data(**kwargs)
        context.update({
            'change_requests': get_change_requests_list_context(),
        })
        return context


class ChangeRequestView(generic_detail.DetailView, TemplateViewWithMenu):
    template_name = 'change_requests/change_request_form.html'
    object = None
    model = VoteChangeRequest
    pk_url_kwarg = 'request_id'
    changes_list = []

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(ChangeRequestView, self).get_context_data(**kwargs)
        context.update({
            'form': EditRequestForm,
            'changes': self.changes_list,
        })
        return context


class ChangeRequestSubmitView(TemplateViewWithMenu):
    template_name = 'change_requests/change_request_submit.html'


class ChangeRequestRejectView(TemplateViewWithMenu):
    template_name = 'change_requests/change_request_reject.html'
