from django.contrib import admin

from apps.moderation_app.models import Reports, VoteChangeRequest, VoteVariantsChangeRequest

admin.site.register(Reports)
admin.site.register(VoteChangeRequest)
admin.site.register(VoteVariantsChangeRequest)
