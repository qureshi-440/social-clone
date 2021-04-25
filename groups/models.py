from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()

class Group(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False,default="",blank=True)
    members = models.ManyToManyField(User,through='GroupMember',related_name='groups_members')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]

class GroupMember(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='memberships')
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.User.username

    class Meta:
        unique_together = ('group','user')
