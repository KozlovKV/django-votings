from django.views.generic import UpdateView

from menu_app.view_subclasses import TemplateViewWithMenu
from django.contrib.auth.models import User
import django.views.generic.edit as generic_edit
from profile_app.models import AdditionUserInfo


class TestProfileView(TemplateViewWithMenu):
    template_name = 'profile_test.html'


class ProfilePageView(TemplateViewWithMenu, generic_edit.UpdateView):  # TODO: унаследовать UpdateView - https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView
    template_name = 'profile_page.html'
    model = AdditionUserInfo
    form_class = ProfilePageForm
    pk_url_kwarg = 'profile_id'

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = self.get_object()

    def get(self, request, *args, **kwargs):
        """
            Добавление уникального для GET-запроса контекста в self.extra_context
            Логика работы с БД
            Да в общем всё что душе угодно (При ненадобности можно вообще удалить)
        """
        return super(ProfilePageView, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile_id': kwargs['profile_id'],
            'profile_user': self.object['profile_user'],
            'votings_created': self.object['votings_created'],
            'number_of_votes_by_user': self.object['number_of_votes_by_user'],
            'user_patronymic': self.object['user_patronymic'],
            'last_website_visited': self.object['last_website_visited'],
        })
        return context
