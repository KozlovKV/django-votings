from django.db import models
from django.contrib.auth.models import User


class Votings(models.Model):
    Title = models.CharField(max_length=256)
    Image = models.FileField()  # ImageField()
    Description = models.TextField()
    Author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    CreationDate = models.DateTimeField(auto_now_add=True)
    EndDate = models.DateTimeField()
    ABSENT = 0
    IN_PROGRESS = 1
    BANNED = 2
    COMPL_STATE_CHOISES = [
        (ABSENT, 'Absent'),
        (IN_PROGRESS, 'in_progress'),
        (BANNED, 'banned'),
    ]
    ComplaintState = models.IntegerField(default=0, choices=COMPL_STATE_CHOISES)
    ALL = 0
    VOTED = 1
    SEE_WHO_CHOISES = [
        (ALL, 'All'),
        (VOTED, 'Voted'),
    ]
    ResultSeeWho = models.IntegerField(default=0, choices=SEE_WHO_CHOISES)
    ANYTIME = 0
    BY_TIMER = 1
    SEE_WHEN_CHOISES = [
        (ANYTIME, 'All'),
        (BY_TIMER, 'Voted'),
    ]
    ResultSeeWhen = models.IntegerField(default=0, choices=SEE_WHEN_CHOISES)
    AnonsCanVote = models.BooleanField()
    ONE = 0
    MANY = 1
    VOTING_TYPE = [
        (ONE, 'One'),
        (MANY, 'Many'),
    ]
    Type = models.IntegerField(default=0, choices=VOTING_TYPE)
    Votes = models.IntegerField()


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


