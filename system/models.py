from email.policy import default
from django.db import models

# Create your models here.
class Role(models.Model):
    id= models.IntegerField(primary_key=True)
    role = models.TextField(default='fan')
class Tier(models.Model):
    id= models.IntegerField(primary_key=True)
    fan_tier = models.TextField(default='fan')
class Permission(models.Model):
    id= models.IntegerField(primary_key=True)
    role = models.TextField(default='fan')
    path = models.TextField(default='/')
class User(models.Model):
    id= models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    date_of_birth = models.TextField()
    fan_tier = models.TextField()
    role = models.TextField(default='fan')
class Salary(models.Model):
     id= models.IntegerField(primary_key=True)
     fan_tier = models.TextField()
     role = models.TextField()
     salary = models.IntegerField(default=0)
     
class Player(models.Model):
    id= models.IntegerField(primary_key=True)
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE, default = None,null=True)
   
class FieldReservation(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.TextField()
    slot_time = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
class AccountSummary(models.Model):
    id = models.IntegerField(primary_key=True)
    transaction_name = models.TextField(default="")
    transaction_amount = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
class Discounts(models.Model):
    id = models.IntegerField(primary_key=True)
    fan_tier = models.TextField()
    discount = models.IntegerField(default=0)
class FanTierFee(models.Model):
    id = models.IntegerField(primary_key=True)
    fan_tier = models.TextField()
    fee = models.IntegerField(default=0)

class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.TextField(default = "XX/XX/XX")
    time = models.TextField(default = "XX:XX")
    team1 = models.TextField(default = "")
    team2 = models.TextField(default = "")
    score1 = models.IntegerField(default = 0)
    score2 = models.IntegerField(default = 0)

class Ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    ticket_type = models.TextField(default = 'General Admission') # we will have also: VIP, Reserved
    price = models.IntegerField(default = 0)
    quantity = models.IntegerField(default = 0)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default = None,null=True)