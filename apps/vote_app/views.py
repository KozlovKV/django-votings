from apps.menu_app.view_subclasses import TemplateViewWithMenu

from apps.vote_app.models import Votings


class VoteListPageView(TemplateViewWithMenu):
    template_name = 'votes/vote_list.html'

    def get_context_data(self, **kwargs):
        context = super(VoteListPageView, self).get_context_data(**kwargs)
        context.update({
            'votings': list(Votings.objects.all()),
        })
        return context
