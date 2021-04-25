# from django.db import models
from django.contrib import auth
from django.contrib.auth import models,mixins
# Create your models here.

class User(models.User,mixins.PermissionRequiredMixin):

    def __str__(self):
        return "@{}".format(self.username)