from django.shortcuts import render
from menu_app.view_menu_context import get_full_menu_context
from menu_app.view_subclasses import TemplateViewWithMenu
from vote_app.forms import VoteConfigForm, ModeledVoteConfigForm

# Create your views here.
from vote_app.models import Votings
from vote_app.models import VoteVariants


def test_page(request):
    context = get_full_menu_context(request)
    return render(request, 'vote_test.html', context)


class VoteListPageView(TemplateViewWithMenu):
    template_name = 'vote_list.html'


# TODO: САМЫЙ ОПТИМАЛЬНЫЙ ВАРИАНТ - https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
def vote_create_page(request):
    context = {'voting_id': -1}
    vote = VoteConfigForm()
    context.update(get_full_menu_context(request))
    context.update({'form': vote})
    if request.POST:
        record = Votings(
            Title=request.POST.get('title'),
            Image=request.POST.get('image'),
            Description=request.POST.get('description'),
            Author=request.POST.get('user'),
            ComplaintState=0,
            ResultSeeWho=request.POST.get('see_who'),
            ResultSeeWhen=request.POST.get('see_when'),
            AnonsCanVote=(request.POST.get('anons_can') == 'True'),
            Type=request.POST.get('type'),
            Votes=0
        )
        record.save()
    # context.update({'history': Votings.objects.all()})
    return render(request, 'vote_config.html', context)


def vote_edit_page(request, voting_id):
    context = {'voting_id': voting_id}

    # TODO: Тут надо будет выгружать в форму данные из Votings
    vote = VoteConfigForm()

    context.update(get_full_menu_context(request))
    context.update({'form': vote})
    if request.POST:
        record = Votings(
            Title=request.POST.get('title'),
            Image=request.POST.get('image'),
            Description=request.POST.get('description'),
            Author=request.POST.get('user'),
            ComplaintState=0,
            ResultSeeWho=request.POST.get('see_who'),
            ResultSeeWhen=request.POST.get('see_when'),
            AnonsCanVote=(request.POST.get('anons_can') == 'True'),
            Type=request.POST.get('type'),
            Votes=0
        )
        record.save()
    # context.update({'history': Votings.objects.all()})
    return render(request, 'vote_config.html', context)


def vote_create_page_alt(request):
    context = {'voting_id': -1}
    vote = ModeledVoteConfigForm()
    context.update(get_full_menu_context(request))
    context.update({'form': vote})
    if request.POST:
        # TODO: сохранение реализуется очень просто, но это чекни в доках сам
        pass
        # record = Votings(
        #     Title=request.POST.get('title'),
        #     Image=request.POST.get('image'),
        #     Description=request.POST.get('description'),
        #     Author=request.POST.get('user'),
        #     ComplaintState=0,
        #     ResultSeeWho=request.POST.get('see_who'),
        #     ResultSeeWhen=request.POST.get('see_when'),
        #     AnonsCanVote=(request.POST.get('anons_can') == 'True'),
        #     Type=request.POST.get('type'),
        #     Votes=0
        # )
        # record.save()
    # context.update({'history': Votings.objects.all()})
    return render(request, 'vote_config.html', context)


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
