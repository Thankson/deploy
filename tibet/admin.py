# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from tibet.models import OpsUser

# Register your models here.

class ForumUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'nickname')
    list_filter = ('is_active', 'is_staff', 'date_joined')

admin.site.register(OpsUser, ForumUserAdmin)