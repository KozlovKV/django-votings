from django.contrib.auth.models import User
from django.db import models


class AdditionUserInfo(models.Model):
    RIGHTS = (
        (0, 'SIMPLE'),
        (1, 'MODERATOR'),
        (2, 'ADMIN'),
    )

    User_id = models.OneToOneField(to=User, on_delete=models.CASCADE)
    votings_created = models.IntegerField(default=0)
    number_of_votes_by_user = models.IntegerField(default=0)
    user_patronymic = models.CharField(max_length=128, default='')
    user_rights = models.IntegerField(default=0, choices=RIGHTS)
    last_website_visited = models.URLField()

    def __str__(self):
        return self.User_id.username
