from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from vote_app.models import Votings


class Reports(models.Model):
    THEMES = [
        (0, 'Жалоба на голосование'),
        (1, 'Сообщение об ошибке'),
    ]

    IN_PROCESS = 0
    SUBMITTED = 1
    REJECTED = 2
    STATUSES = [
        (IN_PROCESS, 'Обрабатывается'),
        (SUBMITTED, 'Решена'),
        (REJECTED, 'Отклонена')
    ]

    Author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    Theme = models.IntegerField(choices=THEMES, default=0)
    Element = models.IntegerField(null=True)  # id модели, соответствующей теме жалобы
    Content = models.TextField()
    Status = models.IntegerField(choices=STATUSES, default=0)
    Create_date = models.DateTimeField(auto_now_add=True)
    Close_date = models.DateTimeField(null=True)

    def is_url_need(self):
        return self.Theme == 0

    def get_object_url_from_report(self):
        if self.is_url_need():
            if self.Theme == 0:
                return reverse_lazy('vote_view', args=(self.Element,))
        else:
            return ''

    def get_humanity_theme_name(self):
        for THEME in self.THEMES:
            if THEME[0] == self.Theme:
                return THEME[1]
        return 'Ошибочная тема'

    @staticmethod
    def get_absolute_url():
        return ''


class VoteChangeRequest(models.Model):
    voting = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    change = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
