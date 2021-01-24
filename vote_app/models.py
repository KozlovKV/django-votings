from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils import timezone

from profile_app.models import AdditionUserInfo


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

    def is_ended(self):
        if self.end_date is None:
            return False
        else:
            return timezone.now() >= self.end_date

    def can_see_result(self, request):
        if self.result_see_when == Votings.BY_TIMER:
            if self.result_see_who == Votings.VOTED:
                return self.is_voted(request.user) and self.is_ended()
            else:
                return self.is_ended()
        else:
            if self.result_see_who == Votings.VOTED:
                return self.is_voted(request.user)
            else:
                return True

    def is_voted(self, request):
        if request.user.is_authenticated:
            votes = Votes.objects.filter(voting=self.pk, user=request.user)
        else:
            votes = Votes.objects.filter(voting=self.pk, fingerprint=request.POST.get('fingerprint', -1))
        return len(votes) > 0

    def can_vote(self, request):
        if self.is_ended():
            self.extra_context.update({
                'reason_cant_vote': 'Голосование закончилось'
            })
            return False
        elif self.is_voted(request):
            self.extra_context.update({
                'reason_cant_vote': 'Вы уже голосовали'
            })
            return False
        elif not request.user.is_authenticated:
            if not self.anons_can_vote:
                self.extra_context.update({
                    'reason_cant_vote': 'Для этого голосования необходимо авторизоваться'
                })
            return self.anons_can_vote
        return True

    def can_edit(self, request):
        if not request.user.is_authenticated:
            return False
        add_info = AdditionUserInfo.objects.get(user=request.user)
        return self.author == request.user or add_info.user_rights == AdditionUserInfo.ADMIN


class VoteVariants(models.Model):
    voting = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    serial_number = models.IntegerField()
    description = models.TextField()
    votes_count = models.IntegerField()

    def get_absolute_url(self):
        return reverse_lazy('vote_view', args=(self.voting,))


class Votes(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True)
    fingerprint = models.CharField(null=True, max_length=256)
    voting = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=VoteVariants, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse_lazy('vote_view', args=(self.voting,))
