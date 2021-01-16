from django.shortcuts import render
from django.urls import reverse, reverse_lazy
import django.views.generic.edit as generic_edit

from menu_app.view_menu_context import get_full_menu_context
from menu_app.view_subclasses import TemplateViewWithMenu
from vote_app.forms import VoteConfigForm, ModeledVoteCreateForm, ModeledVoteEditForm


from vote_app.models import Votings
from vote_app.models import VoteVariants


def test_page(request):
    context = get_full_menu_context(request)
    return render(request, 'vote_test.html', context)


class VoteListPageView(TemplateViewWithMenu):
    template_name = 'vote_list.html'


class CreateVotingView(TemplateViewWithMenu, generic_edit.CreateView):
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

        # Записать ID новго голосования для переадресации
        voting_id = self.object.id
        self.success_url = reverse_lazy('vote_view', args=(voting_id,))
        return post_response


class EditVotingView(TemplateViewWithMenu, generic_edit.FormView):
    template_name = 'vote_config.html'
    object = None  # TODO: принимать существующую запись
    model = Votings
    form_class = ModeledVoteEditForm
    success_url = reverse_lazy('vote_list')

    def get_context_data(self, **kwargs):
        context = super(EditVotingView, self).get_context_data(**kwargs)
        context.update({
            'voting_id': kwargs["voting_id"],
            'context_url': reverse('vote_create', args=(kwargs["voting_id"],)),
        })
        return context

    def post(self, request, *args, **kwargs):
        post_response = super(EditVotingView, self).post(self, request, *args, **kwargs)

        # TODO: Добавить сохранение вариантов голосования и создание записи в модели запросов на редактирование

        # Записать ID новго голосования для переадресации
        voting_id = self.object.id
        self.success_url = reverse_lazy('vote_view', args=(voting_id,))
        return post_response


def get_variants_context(voting_id):
    res = []
    vote_variants = VoteVariants.objects.filter(ID_voting=voting_id)
    voting = Votings.get(pk=voting_id)
    for variant in vote_variants:
        variant_dict = {
            'serial_number': variant.Serial_number,
            'description': variant.Description,
            'votes_count': variant.Counts_of_votes,
            'percent': (variant.Counts_of_votes*100)/voting.Votes,
        }
        res.append(variant_dict)
    res.sort(key=lambda x: x['serial_number'])
    return res


class VotingView(TemplateViewWithMenu, generic_edit.FormView):
    template_name = 'vote_test.html'

    def get_context_data(self, **kwargs):
        context = super(VotingView, self).get_context_data(**kwargs)
        voting_id = kwargs["voting_id"]
        voting_note = Votings.objects.get(pk=voting_id)
        self.success_url = reverse_lazy('vote_view', args=(voting_id,))
        context.update({
            'voting_id': kwargs["voting_id"],
            'title': voting_note.Title,
            'description': voting_note.Description,
            'author': voting_note.Author,
            'status': voting_note.ComplaintState,
            'image': voting_note.Image,
            'resultSeeWho': voting_note.ResultSeeWho,
            'resultSeeWhen': voting_note.ResultSeeWhen,
            'votes_count': voting_note.Votes,
            'end_date': voting_note.EndDate,
            'vote_variants': get_variants_context(voting_id)
        })
        return context

    def post(self, request, *args, **kwargs):
        # TODO: Добавить сохранение вариантов голосования и создание записи в модели запросов на редактирование
        return super(VotingView, self).post(self, request, *args, **kwargs)
