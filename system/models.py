from django.db import models
# from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    date_of_birth = models.TextField()
    fan_tier = models.TextField()
    role = models.TextField(default='fan')
    def __str__(self):
        return self.first_name + ' ' + self.last_name



class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.TextField(default="XX/XX/XX")
    time = models.TextField(default="XX:XX")
    team1 = models.TextField(default="")
    team2 = models.TextField(default="")
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    location = models.TextField(default="")

    
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('article-detail', args = [self.id])

