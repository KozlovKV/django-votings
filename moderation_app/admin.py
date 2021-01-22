from django.contrib import admin

from moderation_app.models import Reports, VoteChangeRequest

admin.site.register(Reports)
admin.site.register(VoteChangeRequest)
