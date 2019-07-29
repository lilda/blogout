from django.db import models
from django.conf import settings
from django.urls.base import reverse
from django.contrib.auth.models import User
import re

# Create your models here.
class Tag(models.Model):
    tag=models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.tag

class News(models.Model):
    
    title=models.CharField(max_length=30)
    content=models.TextField()
    time=models.DateTimeField()
    photo=models.ImageField(upload_to="images/", blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            blank=True,
                                            related_name='like_user_set',
                                            through='Like')
        
    @property
    def like_count(self):
        return self.like_user_set.count()
       
    def __str__ (self):
        return self.title +" - "+ self.content

    def summary(self):
        return self.content[:50]
        
    def get_absolute_url(self):
        return reverse('detail',args=[self.id])  
        
class Comment(models.Model):
    news=models.ForeignKey(News, on_delete=models.CASCADE)
    content=models.TextField()
    time=models.DateTimeField()
    photo=models.ImageField(upload_to="images/", blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-id']

    def __str__ (self):
        return self.content


class Like(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    news=models.ForeignKey(News, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (
             ('user', 'news')
        )

class Hashtag(models.Model):
    news=models.ForeignKey(News, on_delete=models.CASCADE)
    tag=models.ForeignKey(Tag, on_delete=models.PROTECT)
