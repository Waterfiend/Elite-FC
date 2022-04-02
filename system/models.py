from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('article-detail', args = (str(self.id)) )

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    date_of_birth = models.TextField()
    fan_tier = models.TextField()
    role = models.TextField(default='fan')
