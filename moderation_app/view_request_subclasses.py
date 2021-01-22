from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail
from django.utils import timezone

from menu_app.view_menu_context import get_full_site_url
from menu_app.view_subclasses import TemplateViewWithMenu, TemplateEmailSender
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
    template_name = 'change_requests/change_request_one.html'
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


class ChangeRequestCloseTemplateView(TemplateViewWithMenu, generic_edit.FormView):
    template_name = ''
    form_class = EditRequestForm
    success_url = reverse_lazy('moder_change_request_list')
    new_status_name = ''
    change_request_object = None

    def get_email_context(self):
        context = {
            'change_request': self.change_request_object,
            'voting': self.change_request_object.voting,
            'moder': self.request.user,
            'status': self.new_status_name,
            'main_url': get_full_site_url(self.request),
            'date': timezone.now(),
        }
        return context

    def send_close_email(self):
        email = TemplateEmailSender(to=[self.change_request_object.voting.author.email])
        email.subject_template = 'change_requests/email_subject.txt'
        email.body_template = 'change_requests/email_body.txt'
        email.context = self.get_email_context()
        email.request = self.request
        email.send()

    def get(self, request, *args, **kwargs):
        return super(ChangeRequestCloseTemplateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_id = self.kwargs['request_id']
        self.change_request_object = VoteChangeRequest.objects.get(pk=request_id)
        post_resp = super(ChangeRequestCloseTemplateView, self).post(self, request, *args, **kwargs)
        self.send_close_email()
        self.change_request_object.delete()
        return post_resp


class ChangeRequestSubmitView(ChangeRequestCloseTemplateView):
    template_name = 'change_requests/change_request_submit.html'
    new_status_name = 'принят'


class ChangeRequestRejectView(ChangeRequestCloseTemplateView):
    template_name = 'change_requests/change_request_reject.html'
    new_status_name = 'отклонён'
