import copy

from django import forms
from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail

from menu_app.view_menu_context import get_full_menu_context
from menu_app.view_subclasses import TemplateViewWithMenu
from moderation_app.models import VoteChangeRequest, Reports, VoteVariantsChangeRequest
from profile_app.models import AdditionUserInfo
from vote_app.forms import ModeledVoteCreateForm, ModeledVoteEditForm

from vote_app.models import Votings, Votes
from vote_app.models import VoteVariants


def test_page(request):
    context = get_full_menu_context(request)
    return render(request, 'vote_test.html', context)


class VoteListPageView(TemplateViewWithMenu):
    template_name = 'vote_list.html'


class CreateVotingView(generic_edit.CreateView, TemplateViewWithMenu):
    template_name = 'vote_config.html'
    object = None
    model = Votings
    form_class = ModeledVoteCreateForm

    def get_context_data(self, **kwargs):
        context = super(CreateVotingView, self).get_context_data(**kwargs)
        context.update({
            'voting_id': -1,
            'context_url': reverse('vote_create'),
        })
        return context

    def post(self, request, *args, **kwargs):
        post_response = super(CreateVotingView, self).post(self, request, *args, **kwargs)
        self.object.image = self.request.FILES.get('image', None)
        self.object.save()
        self.save_vote_variants()
        return post_response

    def save_vote_variants(self):
        variants_list = get_variants_description_list(self.request)
        variants_count = len(variants_list)
        for serial_number in range(variants_count):
            record = VoteVariants(voting=self.object,
                                  serial_number=serial_number,
                                  description=variants_list[serial_number],
                                  votes_count=0,)
            record.save()


class EditVotingView(generic_edit.UpdateView, TemplateViewWithMenu):
    template_name = 'vote_config.html'
    model = Votings  # and VoteChangeRequest and VoteVariantsChangeRequest
    object = None  # Обрабатываемый объект типа Votings, если только (*), то изменяется, иначе -> old_object
    old_object = None  # Объект типа Votings, содержит в себе неизменную версию object
    new_request = None  # Объект типа VoteChangeRequest, запрос
    form_class = ModeledVoteEditForm
    pk_url_kwarg = 'voting_id'
    old_variants = []  # Список объектов типа VoteVariants со старыми вариантами
    new_variants = []  # Список строк с новыми вариантами
    new_variants_count = 0
    need_clear_votes = False

    def get_object(self, queryset=None):
        object = super(EditVotingView, self).get_object(queryset)
        self.old_variants = list(VoteVariants.objects.filter(voting=object))
        self.old_variants.sort(key=lambda x: x.serial_number)
        return object

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(EditVotingView, self).get_context_data(**kwargs)
        context.update({
            'voting_id': self.object.pk,
            'context_url': reverse('vote_edit', args=(self.object.pk,)),
            'vote_variants': get_variants_context(self.object),
        })
        return context

    def post(self, request, *args, **kwargs):
        self.old_object = Votings.objects.get(pk=kwargs["voting_id"])
        post_response = super(EditVotingView, self).post(self, request, *args, **kwargs)
        if self.is_title_img_or_desc_changed() or self.is_variants_changed():
            print('prinvet mirrr')
            self.save_request()
            self.save_vote_variants()
            self.object = copy.copy(self.old_object)
            self.object.save()
        elif self.is_number_of_variants_changed() or self.is_type_or_anons_changed():
            self.clear_all_votes()
            if self.is_number_of_variants_changed():
                print('Hallo')
                self.save_new_vote_variants()
        return post_response

    def is_type_or_anons_changed(self):
        return self.request.POST.get('type') != self.old_object.type or \
            self.request.POST.get('anons_can_vote') != self.old_object.anons_can_vote

    def is_title_img_or_desc_changed(self):
        return self.request.POST.get('title') != self.old_object.title or \
            self.request.POST.get('image') != self.old_object.image or \
            self.request.POST.get('description') != self.old_object.description

    def is_variants_changed(self):
        need_moderator = False
        self.new_variants = get_variants_description_list(self.request)
        self.new_variants_count = len(self.new_variants)
        if not self.is_number_of_variants_changed():
            for serial_number in range(self.new_variants_count):
                if not need_moderator:
                    need_moderator = self.new_variants[serial_number] != self.old_variants[serial_number].description
        return need_moderator

    def is_number_of_variants_changed(self):
        return self.new_variants_count != len(self.old_variants)

    def save_vote_variants(self):
        for serial_number in range(self.new_variants_count):
            record = VoteVariantsChangeRequest(voting_request=self.new_request,
                                               serial_number=serial_number,
                                               description=self.new_variants[serial_number],)
            record.save()

    def save_new_vote_variants(self):
        VoteVariants.objects.filter(voting=self.object).delete()
        self.object.variants_count = self.new_variants_count
        self.object.save()
        for serial_number in range(self.new_variants_count):
            record = VoteVariants(voting=self.object,
                                  serial_number=serial_number,
                                  description=self.new_variants[serial_number],
                                  votes_count=0,)
            record.save()

    def save_request(self):
        # Здесь нужно отформатировать датувремя, чтобы джанга скушала
        date_str = self.request.POST.get('end_date') if self.request.POST.get('end_date') != '' else None
        self.new_request = VoteChangeRequest(voting=self.object,
                                             title=self.request.POST.get('title'),
                                             image=self.request.POST.get('image'),
                                             description=self.request.POST.get('description'),
                                             end_date=date_str,
                                             result_see_who=self.request.POST.get('result_see_who'),
                                             result_see_when=self.request.POST.get('result_see_when'),
                                             variants_count=self.request.POST.get('variants_count'),
                                             comment=self.request.POST.get('comment'))
        self.new_request.save()

    def clear_all_votes(self):
        for variant in self.old_variants:
            variant.votes_count = 0
        Votes.objects.filter(voting=self.get_object()).delete()
        self.object.voters_count = 0
        self.object.save()


def get_variants_description_list(request):
    res = []
    for serial_num in range(0, int(request.POST.get('variants_count'))):
        res.append(request.POST.get(f'variant_{serial_num}'))
    return res


def get_variants_context(voting):
    res = []
    vote_variants = VoteVariants.objects.filter(voting=voting)
    for variant in vote_variants:
        variant_dict = {
            'serial_number': variant.serial_number,
            'description': variant.description,
            'votes_count': variant.votes_count,
            'percent': (variant.votes_count * 100) / (voting.votes_count if voting.votes_count != 0 else 1),
        }
        res.append(variant_dict)
    res.sort(key=lambda x: x['serial_number'])
    return res


class VotingView(generic_detail.BaseDetailView, TemplateViewWithMenu):
    template_name = 'vote_one.html'
    model = Votings
    object = None
    extra_context = {}
    pk_url_kwarg = 'voting_id'
    variants = []

    def __init__(self):
        super(VotingView, self).__init__()
        self.VOTE_PROCESSORS = {
            'radio': self.vote_one_variant_process,
            'checkbox': self.vote_many_variants_process,
        }

    def get_object(self, queryset=None):
        object = super(VotingView, self).get_object(queryset)
        self.variants = list(VoteVariants.objects.filter(voting=object))
        self.variants.sort(key=lambda x: x.serial_number)
        self.update_votes_count(object)
        return object

    def get_context_data(self, **kwargs):
        context = super(VotingView, self).get_context_data(**kwargs)
        context.update({
            'type_ref': Votings.TYPE_REFS[self.object.type],
            'voting_report': Reports.VOTING_REPORT,
            'can_vote': self.can_vote(self.request.user),
            'can_edit': self.can_edit(self.request.user),
            'can_watch_res': self.can_see_result(),
            'is_ended': self.is_ended(),
            'vote_variants': get_variants_context(self.object),
        })
        try:
            context['img_url'] = self.object.image.url
        except ValueError:
            context['img_url'] = ''
        context.update(self.extra_context)
        return context

    def is_ended(self):
        if self.object.end_date is None:
            return False
        else:
            return timezone.now() >= self.object.end_date

    def can_see_result(self):
        if self.object.result_see_when == Votings.BY_TIMER:
            if self.object.result_see_who == Votings.VOTED:
                return self.is_voted(self.request.user) and self.is_ended()
            else:
                return self.is_ended()
        else:
            if self.object.result_see_who == Votings.VOTED:
                return self.is_voted(self.request.user)
            else:
                return True

    def is_voted(self, user):
        if user.is_authenticated:
            votes = Votes.objects.filter(voting=self.object.pk, user=user)
        else:
            votes = Votes.objects.filter(voting=self.object.pk, fingerprint=self.request.POST.get('fingerprint', -1))
        return len(votes) > 0

    def can_vote(self, user):
        if self.is_ended():
            self.extra_context.update({
                'reason_cant_vote': 'Голосование закончилось'
            })
            return False
        elif self.is_voted(user):
            self.extra_context.update({
                'reason_cant_vote': 'Вы уже голосовали'
            })
            return False
        elif not user.is_authenticated:
            if not self.object.anons_can_vote:
                self.extra_context.update({
                    'reason_cant_vote': 'Для этого голосования необходимо авторизоваться'
                })
            return self.object.anons_can_vote
        return True

    def can_edit(self, user):
        if not user.is_authenticated:
            return False
        add_info = AdditionUserInfo.objects.get(user=user)
        return self.object.author == user or add_info.user_rights == AdditionUserInfo.ADMIN

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.can_vote(request.user) and not self.is_ended():
            self.VOTE_PROCESSORS[Votings.TYPE_REFS[self.object.type]]()
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)

    def vote_one_variant_process(self):
        variant_id = int(self.request.POST.get('variants'))
        variant = self.variants[variant_id]
        new_vote = Votes(voting=self.object, variant=variant)
        if self.request.user.is_authenticated:
            new_vote.user = self.request.user
        else:
            new_vote.fingerprint = self.request.POST.get('fingerprint', None)
        new_vote.save()
        variant.votes_count = len(Votes.objects.filter(variant=variant))
        variant.save()
        self.object.votes_count = len(Votes.objects.filter(voting=self.object))
        self.object.voters_count += 1
        self.object.save()

    def vote_many_variants_process(self):
        for i in range(self.object.variants_count):
            input_val = int(self.request.POST.get(f'{i}', -1))
            if input_val != -1:
                variant = self.variants[input_val]
                new_vote = Votes(voting=self.object, variant=variant)
                if self.request.user.is_authenticated:
                    new_vote.user = self.request.user
                else:
                    new_vote.fingerprint = self.request.POST.get('fingerprint', None)
                new_vote.save()
                variant.votes_count = len(Votes.objects.filter(variant=variant))
                variant.save()
        self.object.votes_count = len(Votes.objects.filter(voting=self.object))
        self.object.voters_count += 1
        self.object.save()

    def update_votes_count(self, object):
        for variant in self.variants:
            variant.votes_count = len(Votes.objects.filter(variant=variant))
            variant.save()
        object.votes_count = len(Votes.objects.filter(voting=object))
        object.save()


class DeleteVotingView(generic_edit.DeleteView, TemplateViewWithMenu):
    template_name = 'vote_delete.html'
    model = Votings
    object = None
    pk_url_kwarg = 'voting_id'
    success_url = reverse_lazy('vote_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.extra_context = {'object': self.object}
        return super(DeleteVotingView, self).get(request, *args, **kwargs)
