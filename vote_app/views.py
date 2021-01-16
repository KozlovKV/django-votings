from django.shortcuts import render
from django.urls import reverse
import django.views.generic.edit as generic_edit

from menu_app.view_menu_context import get_full_menu_context
from menu_app.view_subclasses import TemplateViewWithMenu
from vote_app.forms import VoteConfigForm, ModeledVoteCreateForm, ModeledVoteEditForm

# Create your views here.
from vote_app.models import Votings
from vote_app.models import VoteVariants


def test_page(request):
    context = get_full_menu_context(request)
    return render(request, 'vote_test.html', context)


class VoteListPageView(TemplateViewWithMenu):
    template_name = 'vote_list.html'


# TODO: САМЫЙ ОПТИМАЛЬНЫЙ ВАРИАНТ - https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
# def vote_create_page(request):
#     context = {'voting_id': -1}
#     vote = VoteConfigForm()
#     context.update(get_full_menu_context(request))
#     context.update({'form': vote})
#     if request.POST:
#         record = Votings(
#             Title=request.POST.get('title'),
#             Image=request.POST.get('image'),
#             Description=request.POST.get('description'),
#             Author=request.POST.get('user'),
#             ComplaintState=0,
#             ResultSeeWho=request.POST.get('see_who'),
#             ResultSeeWhen=request.POST.get('see_when'),
#             AnonsCanVote=(request.POST.get('anons_can') == 'True'),
#             Type=request.POST.get('type'),
#             Votes=0
#         )
#         record.save()
#     # context.update({'history': Votings.objects.all()})
#     return render(request, 'vote_config.html', context)


class CreateVotingView(TemplateViewWithMenu, generic_edit.CreateView):
    template_name = 'vote_config.html'
    object = None
    model = Votings
    form_class = ModeledVoteEditForm
    success_url = '/vote/list/'

    def get_context_data(self, **kwargs):
        context = super(CreateVotingView, self).get_context_data(**kwargs)
        context.update({
            'voting_id': -1,
            'context_url': reverse('vote_create'),
        })
        return context

    def post(self, request, *args, **kwargs):
        # TODO: Добавить сохранение вариантов голосования
        return super(CreateVotingView, self).post(self, request, *args, **kwargs)


class EditVotingView(TemplateViewWithMenu, generic_edit.FormView):
    template_name = 'vote_config.html'
    object = None  # TODO: принимать существующую запись
    model = Votings
    form_class = ModeledVoteEditForm
    success_url = '/vote/list/'

    def get_context_data(self, **kwargs):
        context = super(EditVotingView, self).get_context_data(**kwargs)
        context.update({
            'voting_id': kwargs["voting_id"],
            'context_url': reverse('vote_create', args=(kwargs["voting_id"],)),
        })
        return context

    def post(self, request, *args, **kwargs):
        # TODO: Добавить сохранение вариантов голосования и создание записи в модели запросов на редактирование
        return super(EditVotingView, self).post(self, request, *args, **kwargs)


def get_variants_context(voting_id, request):
    res = []
    vote_variants = VoteVariants.objects.filter(ID_voting=voting_id)
    voting = Votings.get(pk=voting_id)
    for variant in vote_variants:
        variant_dict = {'serial_number': variant.Serial_number,
                        'description': variant.Description,
                        'votes_count': variant.Counts_of_votes,
                        'percent': (variant.Counts_of_votes*100)/voting.Votes,
                        }
        res.append(variant_dict)
    res.sort(key=lambda x: x['serial_number'])
    return res

class VotingView(TemplateViewWithMenu, generic_edit.FormView):
    template_name = 'vote_config.html'
    object = None  # TODO: принимать существующую запись
    model = Votings
    form_class = ModeledVoteEditForm
    success_url = '/vote/list/'
    def get_context_data(self, **kwargs):
        context = super(VotingView, self).get_context_data(**kwargs)
        voting_id = kwargs["voting_id"]
        voting_note = Votings.objects.get(pk=voting_id)
        context.update({
            'voting_id': kwargs["voting_id"],
            'context_url': reverse('vote_create', args=(kwargs["voting_id"],)),
            'vote_header' : voting_note.Title,
            'Description': voting_note.Description,
            'Author': voting_note.Author,
            'Status': voting_note.ComplaintState,
            'Image' : voting_note.Image,
            'ResultSeeWho': voting_note.ResultSeeWho,
            'ResultSeeWhen': voting_note.ResultSeeWhen,
            'Vote_counts': voting_note.Votes,
            'End_date' : voting_note.EndDate,
            'vote_variants' : get_variants_context(voting_id, self.request)
        })
        return context

    def post(self, request, *args, **kwargs):
        # TODO: Добавить сохранение вариантов голосования и создание записи в модели запросов на редактирование
        return super(VotingView, self).post(self, request, *args, **kwargs)