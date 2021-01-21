from django import forms
from datetime import timezone
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail

from menu_app.view_menu_context import get_full_menu_context
from menu_app.view_subclasses import TemplateViewWithMenu
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
    for serial_num in range(0, int(request.POST.get('Variants_count'))):
        res.append(request.POST.get(f'variant_{serial_num}'))
    return res


def get_variants_context(voting_id):
    res = []
    vote_variants = VoteVariants.objects.filter(ID_voting=voting_id)
    voting = Votings.objects.get(pk=voting_id)
    for variant in vote_variants:
        variant_dict = {
            'serial_number': variant.Serial_number,
            'description': variant.Description,
            'votes_count': variant.Votes_count,
            'percent': (variant.Votes_count * 100) / voting.Votes_count,
        }
        res.append(variant_dict)
    res.sort(key=lambda x: x['serial_number'])
    return res


class VotingView(generic_detail.BaseDetailView, TemplateViewWithMenu):
    template_name = 'vote_one.html'
    model = Votings
    object = None
    pk_url_kwarg = 'voting_id'
    variants = []

    def get_object(self, queryset=None):
        object = super(VotingView, self).get_object(queryset)
        self.variants = list(VoteVariants.objects.filter(ID_voting=object.pk))
        self.variants.sort(key=lambda x: x.Serial_number)
        return object

    def get_context_data(self, **kwargs):
        context = super(VotingView, self).get_context_data(**kwargs)
        voting_id = self.object.pk
        voting_note = self.object
        context.update({
            'voting_id': voting_id,
            'title': voting_note.Title,
            'description': voting_note.Description,
            'author': voting_note.Author,
            'author_url': reverse_lazy('profile_view', args=(voting_note.Author.id,)),
            'status': voting_note.Complaint_state,
            'image': (voting_note.Image if not voting_note.Image == '' else ''),
            'type': voting_note.Type,
            'type_ref': Votings.TYPE_REFS[voting_note.Type],
            'anons': voting_note.Anons_can_vote,
            'can_vote': self.can_vote(self.request.user),
            'can_watch_res': self.can_see_result(),
            'votes_count': voting_note.Votes_count,
            'end_date': voting_note.End_date,
            'is_ended': self.is_ended(),
            'vote_variants': get_variants_context(voting_id),
        })
        return context

    def is_ended(self, voting_note=None):
        if self.object.End_date == "":
            return False
        else:
            if timezone.now() >= self.object.End_date:
                return True
            elif timezone.now() < self.object.End_date:
                return False

    def can_see_result(self):
        if self.object.Result_see_when == Votings.BY_TIMER:
            return self.is_ended()
        if self.object.Result_see_who == Votings.VOTED:
            return self.is_voted(self.request.user)

    def is_voted(self, user):
        votes = Votes.objects.filter(Voting_id=self.object.pk, User_id=user)
        if len(votes) > 0:
            return True
        else:
            return False

    def can_vote(self, user):
        if self.is_voted(user):
            return False
        if not self.object.Anons_can_vote and not user.is_authenticated:
            return False
        return True

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.can_vote(request.user) and not self.is_ended():
            variant_id = int(request.POST.get('variants').split('_')[1])
            variant = self.variants[variant_id-1]
            new_vote = Votes(User_id=request.user, Voting_id=self.object, Variant_id=variant)
            new_vote.save()
            variant.Votes_count += 1
            variant.save()
            self.object.Votes_count += 1
            self.object.save()
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)
