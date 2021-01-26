from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail
from django.utils import timezone

from menu_app.view_menu_context import get_full_site_url
from menu_app.view_subclasses import TemplateViewWithMenu, TemplateEmailSender
from moderation_app.forms import EditRequestForm
from moderation_app.models import VoteChangeRequest
from profile_app.models import AdditionUserInfo


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


def add_change_note(list_, name, old, new):
    list_.append({
        'name': name,
        'old': old,
        'new': new,
    })


class ChangeRequestView(generic_detail.DetailView, TemplateViewWithMenu):
    template_name = 'change_requests/change_request_one.html'
    object = None
    model = VoteChangeRequest
    pk_url_kwarg = 'request_id'
    changes_list = []

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        self.changes_list = self.get_changes_list()
        context = super(ChangeRequestView, self).get_context_data(**kwargs)
        context.update({
            'form': EditRequestForm,
            'changes': self.changes_list,
        })
        return context

    def get_changes_list(self):
        res = []
        old = self.object.voting
        new_ = self.object
        if old.title != new_.title:
            add_change_note(res, 'Заголовок', old.title, new_.title)
        if old.image != new_.image:
            add_change_note(res, 'Изображение', old.image, new_.image)
        if old.description != new_.description:
            add_change_note(res, 'Описание', old.description, new_.description)
        if old.end_date != new_.end_date:
            add_change_note(res, 'Дата окончания', old.end_date, new_.end_date)
        if old.result_see_who != new_.result_see_who:
            add_change_note(res, 'Кому видны результаты',
                                 old.get_result_see_who_name(),
                                 new_.get_result_see_who_name())
        if old.result_see_when != new_.result_see_when:
            add_change_note(res, 'Когда видны результаты',
                                 old.get_result_see_when_name(),
                                 new_.get_result_see_when_name())
        if old.variants_count != new_.variants_count:
            add_change_note(res, 'Количество вариантов', old.variants_count, new_.variants_count)
        return res


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
            'comment': self.request.POST.get('comment', ''),
            'reset': self.request.POST.get('reset_votes', False),
            'moder': self.request.user,
            'right_name': AdditionUserInfo.objects.get(user=self.request.user).get_right_name(),
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
