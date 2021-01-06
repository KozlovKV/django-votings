from menu_app.view_subclasses import TemplateViewWithMenu

from django.contrib.auth.models import User


class TestProfileView(TemplateViewWithMenu):
    template_name = 'profile_test.html'


class ProfilePageView(TemplateViewWithMenu):
    template_name = 'profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile_id': kwargs['profile_id'],
            'profile_user': User.objects.get(pk=kwargs['profile_id'])
                            if kwargs['profile_id'] != 0 else self.request.user
        })
        return context
