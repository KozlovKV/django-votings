from django import forms
from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail

from menu_app.view_menu_context import get_full_menu_context
from menu_app.view_subclasses import TemplateViewWithMenu
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

        # TODO: Добавить сохранение вариантов голосования
        variants_list = get_variants_description_list(self.request)
        print(variants_list)

        return post_response


class EditVotingView(generic_edit.FormView, TemplateViewWithMenu):
    template_name = 'vote_config.html'
    model = Votings
    form_class = ModeledVoteEditForm

    def get_context_data(self, **kwargs):
        context = super(EditVotingView, self).get_context_data(**kwargs)
        context.update({
            'voting_id': kwargs["voting_id"],
            'context_url': reverse('vote_edit', args=(kwargs["voting_id"],)),
        })
        return context

    def post(self, request, *args, **kwargs):
        post_response = super(EditVotingView, self).post(self, request, *args, **kwargs)

        # TODO: Добавить сохранение вариантов голосования и создание записи в модели запросов на редактирование

        return post_response


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
            'percent': (variant.votes_count * 100) / (voting.voters_count if voting.voters_count != 0 else 1),
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
        self.variants = list(VoteVariants.objects.filter(voting=object.pk))
        self.variants.sort(key=lambda x: x.serial_number)
        return object

    def get_context_data(self, **kwargs):
        context = super(VotingView, self).get_context_data(**kwargs)
        context.update({
            'type_ref': Votings.TYPE_REFS[self.object.type],
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
            if timezone.now() >= self.object.end_date:
                return True
            elif timezone.now() < self.object.end_date:
                return False

    def can_see_result(self):
        if self.object.result_see_when == Votings.BY_TIMER:
            if self.object.result_see_who == Votings.VOTED:
                return self.is_voted(self.request.user) and self.is_ended()
            else:
                return self.is_ended()
        else:
            if self.object.result_see_who == Votings.VOTED:
                return self.is_voted(self.request.user) and self.is_ended()
            else:
                return True

    def is_voted(self, user):
        votes = Votes.objects.filter(voting=self.object.pk, user=user)
        if len(votes) > 0:
            return True
        else:
            return False

    def can_vote(self, user):
        if self.is_ended():
            self.extra_context.update({
                'reason_cant_vote': 'Голосование закончилось'
            })
            return False
        elif not user.is_authenticated:
            if not self.object.anons_can_vote:
                self.extra_context.update({
                    'reason_cant_vote': 'Для этого голосования необходимо авторизоваться'
                })
            return self.object.anons_can_vote
        elif self.is_voted(user):
            self.extra_context.update({
                'reason_cant_vote': 'Вы уже голосовали'
            })
            return False
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
        variant = self.variants[variant_id - 1]
        new_vote = Votes(user=self.request.user, voting=self.object, variant=variant)
        new_vote.save()
        variant.votes_count += 1
        variant.save()
        self.object.voters_count += 1
        self.object.save()

    def vote_many_variants_process(self):
        for i in range(1, self.object.variants_count + 1):
            input_val = int(self.request.POST.get(f'{i}', -1))
            if input_val != -1:
                variant = self.variants[input_val - 1]
                new_vote = Votes(user=self.request.user, voting=self.object, variant=variant)
                new_vote.save()
                variant.votes_count += 1
                variant.save()
                self.object.votes_count += 1
        self.object.voters_count += 1
        self.object.save()
