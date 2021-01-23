from django.urls import reverse_lazy
from django.views.generic import UpdateView

from menu_app.view_subclasses import TemplateViewWithMenu
from django.contrib.auth.models import User
import django.views.generic.edit as generic_edit

from profile_app.forms import ProfilePageForm
from profile_app.models import AdditionUserInfo
from vote_app.models import Votes


class TestProfileView(TemplateViewWithMenu):
    template_name = 'profile_test.html'


class ProfilePageView(TemplateViewWithMenu, generic_edit.UpdateView):  # TODO: унаследовать UpdateView - https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView
    template_name = 'profile_page.html'
    model = User
    object = None
    addition_info = None
    votes = []
    votings = []
    form_class = ProfilePageForm
    pk_url_kwarg = 'profile_id'
    success_url = reverse_lazy('menu')

    def get_object(self, queryset=None):
        object = super(ProfilePageView, self).get_object(queryset)
        self.addition_info = AdditionUserInfo.objects.get(user=self.object)
        self.votes = 0  # TODO: получить список голосов, привязанных к данному пользователю
        self.votings = 0  # TODO: получить список голосований, привязанных к данному пользователю
        self.addition_info.votes_given = 0  # TODO: Обновить количество отданных голосов на основании длины списка голосов
        self.addition_info.votings_created = 0  # TODO: Обновить количество созданных голосований на основании длины списка голосований
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile_id': kwargs['profile_id'],
            'current_user': self.request.user,
            'addition': self.addition_info,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProfilePageView, self).get(request, *args, **kwargs)
