from django.db import models

# Create your models here.

class User(models.Model):
    id= models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    date_of_birth = models.TextField()
    fan_tier = models.TextField()
    role = models.TextField(default='fan')

class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.TextField(default = "XX/XX/XX")
    
def default_match():
    Match.objects.get_or_create(date = "a%/ii/fs")

class Ticket(models.Model):
    
    id = models.IntegerField(primary_key=True)
    ticket_type = models.TextField(default = 'General Admission') # we will have also: VIP, Reserved
    price = models.IntegerField(default = 0)
    quantity = models.IntegerField(default = 0)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default = default_match)