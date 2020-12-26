from django.db import models
from django.contrib.auth.models import User

class Votes(models.Model):
    User_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    Votings_id = models.ForeignKey(to=Votings, on_delete=models.CASCADE)
    Choices_id = models.ForeignKey(to=Choices, on_delete=models.CASCADE)
    Date_vote = models.DateTimeField(auto_now_add=True)

