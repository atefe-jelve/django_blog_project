from django.db import models
from django.shortcuts import reverse


class Post(models.Model):
    CHOICES = (
        ('pub', 'Published'),
        ('drf', 'Draft'),
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=CHOICES, max_length=3)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_details', args=[self.id])











