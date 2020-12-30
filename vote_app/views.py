from django.shortcuts import render
from menu_app.views import get_full_menu_context
from vote_app.forms import VoteConfigForm, ModeledVoteConfigForm

# Create your views here.
from vote_app.models import Votings


def test_page(request):
    context = get_full_menu_context(request)
    return render(request, 'vote_test.html', context)


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

