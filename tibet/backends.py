# coding: utf-8

from django.contrib.auth.backends import ModelBackend # 继承这个为了使用admin的权限控制
from tibet.models import OpsUser

class EmailAuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            user = OpsUser.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except OpsUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return OpsUser.objects.get(pk=user_id)
        except OpsUser.DoesNotExist:
            return None
