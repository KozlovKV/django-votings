from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from vote_app.models import Votings


class Reports(models.Model):
    VOTING_REPORT = 0
    ERROR_MESSAGE = 1
    THEMES = [
        (VOTING_REPORT, 'Жалоба на голосование'),
        (ERROR_MESSAGE, 'Сообщение об ошибке'),
    ]

    IN_PROCESS = 0
    SUBMITTED = 1
    REJECTED = 2
    STATUSES = [
        (IN_PROCESS, 'Обрабатывается'),
        (SUBMITTED, 'Решена'),
        (REJECTED, 'Отклонена')
    ]

    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    theme = models.IntegerField(choices=THEMES, default=0)
    element = models.IntegerField(null=True, blank=True)  # id модели, соответствующей теме жалобы
    content = models.TextField()
    status = models.IntegerField(choices=STATUSES, default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True, blank=True)

    def is_url_need(self):
        return self.theme == 0

    def get_object_url_from_report(self):
        if not self.is_url_need():
            return ''
        if self.theme == 0 and self.element is not None:
            return reverse_lazy('vote_view', args=(self.element,))
        else:
            return ''

    def get_humanity_theme_name(self):
        for THEME in self.THEMES:
            if THEME[0] == self.theme:
                return THEME[1]
        return 'Ошибочная тема'

    def get_humanity_status_name(self):
        for STATUS in self.STATUSES:
            if STATUS[0] == self.status:
                return STATUS[1]
        return 'Ошибочный статус'

    @staticmethod
    def get_absolute_url():
        return reverse_lazy('moder_report_send')


class VoteChangeRequest(models.Model):
    voting = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    change = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
