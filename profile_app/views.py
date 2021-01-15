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
    queryset = AdditionUserInfo.objects.all()
    
    
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
            'profile_user': User.objects.GET(pk=kwargs['profile_id'])
                            if kwargs['profile_id'] != 0 else self.request.user,
            'votings_created': User.objects.GET('votings_created')
                            if kwargs['profile_id'] != 0 else self.request.user,
            'number_of_votes_by_user': User.objects.GET('number_of_votes_by_user')
                            if kwargs['profile_id'] != 0 else self.request.user,
            'user_patronymic': User.objects.GET('user_patronymic')
                            if kwargs['profile_id'] != 0 else self.request.user,
            'last_website_visited': User.objects.GET('last_website_visited')
                            if kwargs['profile_id'] != 0 else self.request.user,
        })
        return context
