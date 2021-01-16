from django.db import models
from django.contrib.auth.models import User


class Votings(models.Model):
    Title = models.CharField(max_length=256)
    Image = models.ImageField(upload_to='images/', blank=True, null=True)  # FileField()
    Description = models.TextField()
    Author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    CreationDate = models.DateTimeField(auto_now_add=True)
    EndDate = models.DateTimeField(blank=True, null=True)
    ABSENT = 0
    IN_PROGRESS = 1
    BANNED = 2
    COMPL_STATE_CHOICES = [
        (ABSENT, 'Отсутствует'),
        (IN_PROGRESS, 'На рассмотрении'),
        (BANNED, 'Забанено'),
    ]
    ComplaintState = models.IntegerField(default=0, choices=COMPL_STATE_CHOICES)
    ALL = 0
    VOTED = 1
    SEE_WHO_CHOICES = [
        (ALL, 'Всем'),
        (VOTED, 'Проголосовавшим'),
    ]
    ResultSeeWho = models.IntegerField(null=True, default=0, choices=SEE_WHO_CHOICES)
    ANYTIME = 0
    BY_TIMER = 1
    SEE_WHEN_CHOICES = [
        (ANYTIME, 'В любое время'),
        (BY_TIMER, 'После окончания'),
    ]
    ResultSeeWhen = models.IntegerField(null=True, default=0, choices=SEE_WHEN_CHOICES)
    AnonsCanVote = models.BooleanField(default=False)
    ONE = 0
    MANY = 1
    VOTING_TYPE = [
        (ONE, 'Один вариант'),
        (MANY, 'Много вариантов'),
    ]
    Type = models.IntegerField(default=0, choices=VOTING_TYPE)
    Votes = models.IntegerField(default=0)


class VoteVariants(models.Model):
    ID_voting = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    Serial_number = models.IntegerField()
    Description = models.TextField()
    Counts_of_votes = models.IntegerField()


class Votes(models.Model):
    User_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    Votings_id = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    Choices_id = models.ForeignKey(to=VoteVariants, on_delete=models.CASCADE)
    Date_vote = models.DateTimeField(auto_now_add=True)


class VoteChangeRequest(models.Model):
    voting_id = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    Change = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()


