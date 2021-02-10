from django.shortcuts import render
from django.urls import reverse_lazy

import django.views.generic.edit as generic_edit
import django.views.generic.detail as generic_detail
from apps.menu_app.view_subclasses import TemplateViewWithMenu

from apps.moderation_app.models import Reports
from apps.vote_app.models import Votings, Votes, VoteVariants


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
    template_name = 'votes/vote_one.html'
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
        object.update_votes_count()
        object.update_voters_count()
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
        context.update(self.extra_context)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.can_vote(request) and not self.object.is_ended():
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


class DeleteVotingView(generic_edit.DeleteView, TemplateViewWithMenu):
    template_name = 'votes/vote_delete.html'
    model = Votings
    object = None
    pk_url_kwarg = 'voting_id'
    success_url = reverse_lazy('vote_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.extra_context = {'object': self.object}
        return super(DeleteVotingView, self).get(request, *args, **kwargs)
