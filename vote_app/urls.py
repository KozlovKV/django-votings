from django.urls import path
import vote_app.views as vote


urlpatterns = [
    path('list/', vote.VoteListPageView.as_view(), name='vote_list'),
    path('create/', vote.CreateVotingView.as_view(), name='vote_create'),
    path('edit/<int:voting_id>/', vote.EditVotingView.as_view(), name='vote_edit'),
    path('delete/<int:voting_id>/', vote.DeleteVotingView.as_view(), name='vote_delete'),
    path('view/<int:voting_id>/', vote.VotingView.as_view(), name='vote_view'),
]