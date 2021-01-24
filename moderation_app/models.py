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
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='voting_images/', blank=True, null=True)  # FileField()
    description = models.TextField()
    end_date = models.DateTimeField(blank=True, null=True)

    ALL = 0
    VOTED = 1
    SEE_WHO_CHOICES = [
        (ALL, 'Всем'),
        (VOTED, 'Проголосовавшим'),
    ]
    result_see_who = models.IntegerField(null=True, default=0, choices=SEE_WHO_CHOICES)

    ANYTIME = 0
    BY_TIMER = 1
    SEE_WHEN_CHOICES = [
        (ANYTIME, 'В любое время'),
        (BY_TIMER, 'После окончания'),
    ]
    result_see_when = models.IntegerField(null=True, default=0, choices=SEE_WHEN_CHOICES)

    variants_count = models.IntegerField(default=2)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def get_absolute_url(self):
        return reverse_lazy('vote_view', args=(self.pk,))

    def get_result_see_who_name(self):
        for note in self.SEE_WHO_CHOICES:
            if note[0] == self.result_see_who:
                return note[1]

    def get_result_see_when_name(self):
        for note in self.SEE_WHEN_CHOICES:
            if note[0] == self.result_see_when:
                return note[1]


class VoteVariantsChangeRequest(models.Model):
    voting_request = models.ForeignKey(to=VoteChangeRequest, on_delete=models.CASCADE)
    serial_number = models.IntegerField()
    description = models.TextField()
    votes_count = models.IntegerField()

    def get_absolute_url(self):
        return reverse_lazy('vote_view', args=(self.voting,))
