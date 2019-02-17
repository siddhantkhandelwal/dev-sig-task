from django.contrib import admin
from .models import Team, Member, Question
from django.contrib.auth.models import Group

class TeamAdmin(admin.ModelAdmin):
    list_display = ['user', 'rank', 'score']
    search_fields= ['rank']

class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'team']
    search_fields = ['id']

admin.autodiscover()
admin.site.register(Team, TeamAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.unregister(Group)
admin.site.register(Question)
