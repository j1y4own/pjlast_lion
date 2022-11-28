from cgitb import text
from email.mime import image
from pyexpat import model
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import User
from cuapp.models import CustomUser

class Cashbook(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    email = models.EmailField(max_length=254, blank=True)
    url = models.URLField(max_length=200, blank= True)
    created_at = models.DateTimeField(default= datetime.now, blank=True)
    image = models.ImageField(upload_to = 'image/', blank = True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author')
    post_like = models.ManyToManyField(CustomUser, related_name='like_user', blank = True)
    like_count = models.PositiveIntegerField(default = 0)
    hashtags = models.ManyToManyField('Hashtag', blank= True)
    def __str__(self):
        return self.title

    def clean(self):
        title = self.title
        if title =="":
            raise ValidationError("글을 작성해주세요")
        return super(Cashbook,self).clean()
    
def clean_content(self):
    instance = getattr(self, 'instance', None)
    if instance and instance.pk:
        return instance.content
    else:
        return self.cleaned_data['email']

class Comment(models.Model):
    def __str__(self):
        return self.text

    author = models.ForeignKey('cuapp.CustomUser', on_delete=models.CASCADE, blank=True, null = True)
    cashbook_id = models.ForeignKey(Cashbook, on_delete = models.CASCADE, related_name='comments', null = True)
    text = models.CharField(max_length=50)

class Hashtag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
