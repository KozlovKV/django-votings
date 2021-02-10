from django.contrib.auth.models import User
from django.db import models


class AdditionUserInfo(models.Model):
    SIMPLE = 0
    MODER = 1
    ADMIN = 2
    RIGHTS = (
        (SIMPLE, 'Обычный'),
        (MODER, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    votings_created = models.IntegerField(default=0)
    votes_given = models.IntegerField(default=0)
    user_rights = models.IntegerField(choices=RIGHTS, default=0)
    last_website_visited = models.URLField()

    def __str__(self):
        return self.user.username

    def get_right_name(self):
        for right_note in self.RIGHTS:
            if right_note[0] == self.user_rights:
                return right_note[1]
