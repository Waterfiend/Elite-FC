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

class Ticket(models.Model):
    
    number = models.IntegerField(primary_key=True)
    ticket_type = models.TextField(default = 'General Admission') # we will have also: VIP, Reserved

    def __init__(self, num, typ):
        self.number = num
        self.ticket_type = typ

    def __str__(self):
        return self.ticket_type
