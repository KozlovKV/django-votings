from enum import Enum

from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail
from django.utils import timezone

from apps.menu_app.view_menu_context import get_full_site_url
from apps.menu_app.view_subclasses import TemplateViewWithMenu, TemplateEmailSender
from apps.moderation_app.forms import EditRequestForm
from apps.moderation_app.models import VoteChangeRequest, VoteVariantsChangeRequest
from apps.profile_app.models import AdditionUserInfo
from vote_app.models import Votes, VoteVariants


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


class ChangePatterns(Enum):
    TITLE = ('title', 'Заголовок')
    IMAGE = ('image', 'Изображение')
    DESCRIPTION = ('description', 'Описание')
    END_DATE = ('end_date', 'Дата окончания')
    VARIANTS_COUNT = ('variants_count', 'Количество вариантов')


def add_change_note(list_, name, old, new):
    list_.append({
        'name': name,
        'old': old,
        'new': new,
    })


def get_fields_change_list(old, new_):
    res = []
    old_dict = old.__dict__
    new_dict = new_.__dict__
    for field_pattern in ChangePatterns:
        old_note = old_dict[field_pattern.value[0]]
        new_note = new_dict[field_pattern.value[0]]
        if old_note != new_note:
            add_change_note(res, field_pattern.value[1], old_note, new_note)
    if old.result_see_who != new_.result_see_who:
        add_change_note(res, 'Кому видны результаты',
                        old.get_result_see_who_name(),
                        new_.get_result_see_who_name())
    if old.result_see_when != new_.result_see_when:
        add_change_note(res, 'Когда видны результаты',
                        old.get_result_see_when_name(),
                        new_.get_result_see_when_name())
    return res


def get_variants_change_list(old, new_):
    res = []
    old_variants = VoteVariants.objects.filter(voting=old)
    new_variants = VoteVariantsChangeRequest.objects.filter(voting_request=new_)
    empty_variant = VoteVariantsChangeRequest(
        voting_request=new_,
        description='Пусто',
        serial_number=0,
    )
    for i in range(max(len(old_variants), len(new_variants))):
        old_variant = old_variants[i] if i < len(old_variants) else empty_variant
        new_variant = new_variants[i] if i < len(new_variants) else empty_variant
        if old_variant.description != new_variant.description:
            add_change_note(res, f'Вариант {i + 1}', old_variant.description, new_variant.description)
    return res


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
            'image_label': ChangePatterns.IMAGE.value[1],
        })
        return context

    def get_changes_list(self):
        old = self.object.voting
        new_ = self.object
        res = get_fields_change_list(old, new_)
        res += get_variants_change_list(old, new_)
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


def save_new_voting(request_object, reset=False):
    voting = request_object.voting
    new_ = request_object
    voting.title = new_.title
    voting.image = new_.image
    voting.description = new_.description
    voting.end_date = new_.end_date
    voting.result_see_who = new_.result_see_who
    voting.result_see_when = new_.result_see_when
    voting.variants_count = new_.variants_count
    old_variants = VoteVariants.objects.filter(voting=voting)
    new_variants = VoteVariantsChangeRequest.objects.filter(voting_request=new_)
    empty_variant = VoteVariantsChangeRequest(
        voting_request=new_,
        description='Пусто',
        serial_number=0,
    )
    for i in range(new_.variants_count):
        variant = old_variants[i] if i < len(old_variants) else empty_variant
        variant.description = new_variants[i].description
        variant.save()
    if reset:
        Votes.objects.filter(voting=voting).delete()
        voting.voters_count = 0
        voting.save()
    voting.save()


class ChangeRequestSubmitView(ChangeRequestCloseTemplateView):
    template_name = 'change_requests/change_request_submit.html'
    new_status_name = 'принят'

    def post(self, request, *args, **kwargs):
        request_id = self.kwargs['request_id']
        self.change_request_object = VoteChangeRequest.objects.get(pk=request_id)
        post_resp = super(ChangeRequestSubmitView, self).post(self, request, *args, **kwargs)
        save_new_voting(self.change_request_object, self.request.POST.get('reset_votes', False))
        self.send_close_email()
        self.change_request_object.delete()
        return post_resp


class ChangeRequestRejectView(ChangeRequestCloseTemplateView):
    template_name = 'change_requests/change_request_reject.html'
    new_status_name = 'отклонён'

    def post(self, request, *args, **kwargs):
        request_id = self.kwargs['request_id']
        self.change_request_object = VoteChangeRequest.objects.get(pk=request_id)
        post_resp = super(ChangeRequestCloseTemplateView, self).post(self, request, *args, **kwargs)
        self.send_close_email()
        self.change_request_object.delete()
        return post_resp
