from django.db import models

from django.contrib.auth.models import User

class UserInfo(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, null=True)
    birth = models.CharField(max_length=150, null=True)
    school = models.CharField(max_length=300, null=True)
    number = models.CharField(max_length=200, null=True)
    mbti = models.CharField(max_length=150, null=True)
    hobby = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name: '사용자정보'
        verbose_name_plural = '사용자정보'
        ordering = ['username', ]

    def __str__(self):
        return self.address