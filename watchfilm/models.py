# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import os
from watchfilms import settings


# Create your models here.
class UserProfile(models.Model):  # 用户信息表单，包含头像
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT, 'avatar'), verbose_name='用户头像', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user)


class UserMovieSeen(models.Model):  # 用户已经观看的影单
    user = models.ForeignKey(User)
    seen = models.IntegerField('看过的电影')

    def __unicode__(self):
        return unicode(self.user)


class UserMovieList(models.Model):  # 用户添加的豆瓣电影
    user = models.ForeignKey(User)
    movie_id = models.IntegerField('添加的电影')

    def __unicode__(self):
        return unicode(self.user)


class UserAddList(models.Model):  # 用户自己添加的影视
    user = models.ForeignKey(User)
    name = models.CharField('影视标题', max_length=30)
    describe = models.TextField('简述', null=True, blank=True)
    url = models.URLField('链接')

    def __unicode__(self):
        return unicode(self.user)




