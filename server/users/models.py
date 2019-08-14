from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    mobile = models.CharField(max_length=11, verbose_name="电话")
    join_date = models.DateField()

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

def get_or_create_userprofile(user):
    if user:
        # up = get_object_or_404(UserProfile, user=user)
        try:
            up = UserProfile.objects.get(user=user)
            if up:
                return up
        except ObjectDoesNotExist:
            pass
    up = UserProfile(user=user, join_date=timezone.now())
    up.save()
    return up


User.profile = property(lambda u: get_or_create_userprofile(user=u))


class ImageCode(models.Model):
    codeid = models.CharField(max_length=40, verbose_name='验证码ID')
    code = models.CharField(max_length=10, verbose_name='验证码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "图片验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
