from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class Votings(models.Model):
    Title = models.CharField(max_length=256)
    Image = models.ImageField(upload_to='voting_images/', blank=True, null=True)  # FileField()
    Description = models.TextField()
    Author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    Creation_date = models.DateTimeField(auto_now_add=True)
    End_date = models.DateTimeField(blank=True, null=True)
    ABSENT = 0
    IN_PROGRESS = 1
    BANNED = 2
    COMPL_STATE_CHOICES = [
        (ABSENT, 'Отсутствует'),
        (IN_PROGRESS, 'На рассмотрении'),
        (BANNED, 'Забанено'),
    ]
    Complaint_state = models.IntegerField(default=0, choices=COMPL_STATE_CHOICES)
    ALL = 0
    VOTED = 1
    SEE_WHO_CHOICES = [
        (ALL, 'Всем'),
        (VOTED, 'Проголосовавшим'),
    ]
    Result_see_who = models.IntegerField(null=True, default=0, choices=SEE_WHO_CHOICES)
    ANYTIME = 0
    BY_TIMER = 1
    SEE_WHEN_CHOICES = [
        (ANYTIME, 'В любое время'),
        (BY_TIMER, 'После окончания'),
    ]
    Result_see_when = models.IntegerField(null=True, default=0, choices=SEE_WHEN_CHOICES)
    Anons_can_vote = models.BooleanField(default=False)
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
    Type = models.IntegerField(default=0, choices=VOTING_TYPE)
    Votes_count = models.IntegerField(default=0)
    Variants_count = models.IntegerField(default=2)

    def get_absolute_url(self):
        return reverse_lazy('vote_view', args=(self.pk, ))


class VoteVariants(models.Model):
    ID_voting = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    Serial_number = models.IntegerField()
    Description = models.TextField()
    Votes_count = models.IntegerField()


class Votes(models.Model):
    User_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    Voting_id = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    Variant_id = models.ForeignKey(to=VoteVariants, on_delete=models.CASCADE)
    Date_vote = models.DateTimeField(auto_now_add=True)
