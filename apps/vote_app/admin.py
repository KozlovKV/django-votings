from django.contrib import admin

# Register your models here.
from apps.vote_app.models import Votings, VoteVariants, Votes

admin.site.register(Votings)
admin.site.register(VoteVariants)
admin.site.register(Votes)
