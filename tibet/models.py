# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class RestartManager(models.Manager):
    def get_all_restart_by_time(self):
        query = self.get_queryset().\
                all().order_by('-applitime')
        return query

class RestartJobs(models.Model):
    #operator = models.ForeignKey(OpsUser, related_name='restart_operator', null=True, blank=True)
    applicant = models.CharField(max_length=128, null=True, blank = True)
    applitime = models.DateTimeField(auto_now=True)
    projects = models.CharField(max_length=128, null=True, blank = True)
    jenksins_job_name = models.CharField(max_length=128, null=True, blank = True)
    jenksins_job_number = models.IntegerField(null=True, blank=True)
    operator = models.CharField(max_length=128, null=True, blank=True)
    restarttime = models.DateTimeField(null=True, blank = True)
    note = models.CharField(max_length=128, null=True, blank = True)
    class Meta:
        ordering = ['-applitime']
    objects = RestartManager()

class jids(models.Model):
    jid = models.CharField(max_length=255, unique=True)
    load = models.TextField(max_length=1024)

    def __unicode__(self):
        return self.jid

    class Meta:
        db_table = 'jids'
        ordering = ('-jid',)


class salt_events(models.Model):
    tag = models.CharField(max_length=255)
    data = models.CharField(max_length=1024)
    alter_time = models.DateTimeField(auto_now_add=True)
    master_id = models.CharField(max_length=255)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = 'salt_events'
        ordering = ('-id',)


class salt_returns(models.Model):
    custom_id = models.AutoField(primary_key=True)
    fun = models.CharField(max_length=50)
    jid = models.CharField(max_length=255)
    return_char = models.TextField(max_length=1024, db_column='return')
    id = models.CharField(max_length=50)
    success = models.CharField(max_length=10)
    full_ret = models.TextField(max_length=1024)
    alter_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.custom_id


    class Meta:
        db_table = 'salt_returns'
        ordering = ('-custom_id',)