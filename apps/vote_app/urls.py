from django.urls import path
import apps.vote_app.views as vote_main
import apps.vote_app.view_vote_config_subclasses as vote_config
import apps.vote_app.view_vote_one_subclasses as vote_one


urlpatterns = [
    path('list/', vote_main.VoteListPageView.as_view(), name='vote_list'),
    path('create/', vote_config.CreateVotingView.as_view(), name='vote_create'),
    path('edit/<int:voting_id>/', vote_config.EditVotingView.as_view(), name='vote_edit'),
    path('delete/<int:voting_id>/', vote_one.DeleteVotingView.as_view(), name='vote_delete'),
    path('view/<int:voting_id>/', vote_one.VotingView.as_view(), name='vote_view'),
]