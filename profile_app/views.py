from menu_app.view_subclasses import TemplateViewWithMenu

from django.contrib.auth.models import User


class TestProfileView(TemplateViewWithMenu):
    template_name = 'profile_test.html'


class ProfilePageView(TemplateViewWithMenu):  # TODO: унаследовать UpdateView - https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView
    template_name = 'profile_page.html'

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
            'profile_user': User.objects.get(pk=kwargs['profile_id'])
                            if kwargs['profile_id'] != 0 else self.request.user
        })
        return context
