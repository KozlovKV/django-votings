from django.db import models

# Create your models here.
class AdditionUserInfo(models.Model):
    RIGHTS = (
        (0, 'SIMPLE'),
        (1, 'MODERATOR'),
        (2, 'ADMIN'),
    )

    User_id = models.OneToOneField(User.ID)
    votings_created = models.IntegerField()
    number_of_votes_by_user = models.IntegerField()
    user_patronymic = models.CharField(max_length=128)
    user_rights = models.IntegerField(default=0, choices=RIGHTS)
    last_website_visited = models.URLField()
    
    def __str__(self):
        return self.User.username
