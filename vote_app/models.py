from django.db import models
from vote_app.models import Votings


class Vote_Variants(models.Model):
    ID_voting = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    Serial_number = models.IntegerField()
    Description = models.TextField()
    Counts_of_votes = models.IntegerField()
