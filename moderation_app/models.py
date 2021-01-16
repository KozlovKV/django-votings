from audioop import reverse

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class Reports(models.Model):
    THEMES = [
        (0, 'Жалоба на голосование'),
        (1, 'Сообщение об ошибке'),
    ]

    STATUSES = [
        (0, 'Обрабатывается'),
        (1, 'Решена'),
        (2, 'Отклонена')
    ]

    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    theme = models.IntegerField(choices=THEMES)
    element = models.IntegerField(null=True)  # id модели, соответствующей теме жалобы
    content = models.TextField()
    status = models.IntegerField(choices=STATUSES)
    create_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True)

    def is_url_need(self):
        return self.theme == 0

    def get_object_url_from_report(self):
        if self.is_url_need():
            if self.theme == 0:
                return reverse_lazy('vote_view', args=(self.element,))
        else:
            return ''

    def get_humanity_theme_name(self):
        for THEME in self.THEMES:
            if THEME[0] == self.theme:
                return THEME[1]
        return 'Ошибочная тема'