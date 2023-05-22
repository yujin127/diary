from django.db import models
from datetime import datetime

class Diary(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'[{self.created_at}] {self.title}'

    def get_absolute_urls(self):
        return f'/diary/{self.pk}/'
