from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class Votings(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='voting_images/', blank=True, null=True)  # FileField()
    description = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    ABSENT = 0
    IN_PROGRESS = 1
    BANNED = 2
    COMPL_STATE_CHOICES = [
        (ABSENT, 'Отсутствует'),
        (IN_PROGRESS, 'На рассмотрении'),
        (BANNED, 'Забанено'),
    ]
    complaint_state = models.IntegerField(default=0, choices=COMPL_STATE_CHOICES)

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

    anons_can_vote = models.BooleanField(default=False)

    ONE = 0
    MANY = 1
    VOTING_TYPE = [
        (ONE, 'Один вариант'),
        (MANY, 'Много вариантов'),
    ]
    TYPE_REFS = {
        ONE: 'radio',
        MANY: 'checkbox',
    }
    type = models.IntegerField(default=0, choices=VOTING_TYPE)

    voters_count = models.IntegerField(default=0)
    votes_count = models.IntegerField(default=0)
    variants_count = models.IntegerField(default=2)

    def get_absolute_url(self):
        return reverse_lazy('vote_view', args=(self.pk, ))

    def get_result_see_who_name(self):
        for note in self.SEE_WHO_CHOICES:
            if note[0] == self.result_see_who:
                return note[1]

    def get_result_see_when_name(self):
        for note in self.SEE_WHEN_CHOICES:
            if note[0] == self.result_see_when:
                return note[1]


class VoteVariants(models.Model):
    voting = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    serial_number = models.IntegerField()
    description = models.TextField()
    votes_count = models.IntegerField()

    def get_absolute_url(self):
        return reverse_lazy('vote_view', args=(self.voting,))


class Votes(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    voting = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=VoteVariants, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse_lazy('vote_view', args=(self.voting,))
