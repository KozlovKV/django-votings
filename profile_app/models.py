from django.contrib.auth.models import User
from django.db import models


class AdditionUserInfo(models.Model):
    RIGHTS = (
        (0, 'Обычный'),
        (1, 'Модератор'),
        (2, 'Администратор'),
    )

    User_id = models.OneToOneField(to=User, on_delete=models.CASCADE)
    votings_created = models.IntegerField(default=0)
    number_of_votes_by_user = models.IntegerField(default=0)
    user_patronymic = models.CharField(max_length=128, default='')
    user_rights = models.IntegerField(choices=RIGHTS, default=0)
    last_website_visited = models.URLField()

    def __str__(self):
        return self.User_id.username

    def get_right_name(self):
        for right_note in self.RIGHTS:
            if right_note[0] == self.user_rights:
                return right_note[1]
