from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Diary(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None

    def __str__(self):
        return f'[{self.created_at}] {self.title}'

    def get_absolute_urls(self):
        return f'/diary/diary_detail/{self.pk}/'
