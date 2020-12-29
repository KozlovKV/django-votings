from django.shortcuts import render
from menu_app.views import get_full_menu_context
from vote_app.forms import VoteConfigForm

# Create your views here.
from vote_app.models import Votings


def test_page(request):
    context = get_full_menu_context(request)
    return render(request, 'vote_test.html', context)


def vote_config_page(request):
    context = {}
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
