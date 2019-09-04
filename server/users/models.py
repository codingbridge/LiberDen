from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    GENDER = [('m', 'Male'), ('f','Female'),('s', 'Secret')]
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    gender = models.CharField(null=True, blank=True, max_length=6, choices=GENDER,
                              verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    mobile = models.CharField(max_length=11, unique=True, verbose_name="电话")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
