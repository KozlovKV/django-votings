from django import forms
from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail

from menu_app.view_menu_context import get_full_menu_context
from menu_app.view_subclasses import TemplateViewWithMenu
from moderation_app.models import VoteChangeRequest, Reports
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
    model = Votings  # and VoteChangeRequest
    object = None
    old_object = None
    form_class = ModeledVoteEditForm
    pk_url_kwarg = 'voting_id'
    need_moderator = False
    variants = []

    def get_object(self, queryset=None):
        object = super(EditVotingView, self).get_object(queryset)
        self.variants = list(VoteVariants.objects.filter(voting=object))
        self.variants.sort(key=lambda x: x.serial_number)
        return object

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        self.old_object = self.object
        context = super(EditVotingView, self).get_context_data(**kwargs)
        context.update({
            'voting_id': self.object.pk,
            'can_edit': self.object.can_edit(self.request),
            'context_url': reverse('vote_edit', args=(self.object.pk,)),
            'vote_variants': get_variants_context(self.object),
        })
        return context

    def post(self, request, *args, **kwargs):
        post_response = super(EditVotingView, self).post(self, request, *args, **kwargs)
        self.save_change_request()
        if self.need_moderator:
            self.object = self.old_object
        return post_response

    def save_change_request(self):
        if self.request.POST.get('title') != self.object.title or \
                self.request.POST.get('image') != self.object.image or \
                self.request.POST.get('description') != self.object.description:
            self.need_moderator = True

        # Здесь должно быть сравнение старых вариантов голосования и новых
        # если изменения есть - self.need_moderator = True

        if self.need_moderator:
            record = VoteChangeRequest(voting=self.object,
                                       title=self.request.POST.get('title'),
                                       image=self.request.POST.get('image'),
                                       description=self.request.POST.get('description'),
                                       end_date=self.request.POST.get('end_date'),
                                       result_see_who=self.request.POST.get('result_see_who'),
                                       result_see_when=self.request.POST.get('result_see_when'),
                                       variants_count=self.request.POST.get('variants_count'),
                                       comment=self.request.POST.get('comment'))
            record.save()


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
            'can_vote': self.object.can_vote(self.request),
            'reason_cant_vote': self.object.get_reason_cant_vote(self.request),
            'can_edit': self.object.can_edit(self.request),
            'can_watch_res': self.object.can_see_result(self.request),
            'is_ended': self.object.is_ended(),
            'vote_variants': get_variants_context(self.object),
        })
        try:
            context['img_url'] = self.object.image.url
        except ValueError:
            context['img_url'] = ''
        context.update(self.extra_context)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.can_vote(request.user) and not self.object.is_ended():
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
