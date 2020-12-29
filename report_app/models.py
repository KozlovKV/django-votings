from django.db import models
from django.contrib.auth.models import User


class Reports(models.Model):
    STATUSES = [
        (0, 'IN_PROCESS'),
        (1, 'RESOLVED'),
        (2, 'REJECTED')
    ]

    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=256)
    element = models.IntegerField(null=True)  # id модели, соответствующей теме жалобы
    content = models.TextField()
    status = models.IntegerField(choices=STATUSES)
    create_date = models.DateTimeField(auto_now_add=True)
    # close_date = models.DateTimeField()
