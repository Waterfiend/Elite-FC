from email.policy import default
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from operator import mod

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
class Salary(models.Model):
     id= models.IntegerField(primary_key=True)
     fan_tier = models.TextField()
     role = models.TextField()
     salary = models.IntegerField(default=0)
class FieldReservation(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.TextField()
    slot_time = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
class AccountSummary(models.Model):
    # id = models.IntegerField(primary_key=True)
    transaction_name = models.TextField(default="")
    transaction_amount = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    date = models.TextField(default="")
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
    location = models.TextField(default="")
    
    def team1Img(self):
        try:
            team1_img_url = Team.objects.filter(name=self.team1).first().image.url
        except:
            team1_img_url=''
        return team1_img_url
    def team2Img(self):
        try:
            team2_img_url = Team.objects.filter(name=self.team2).first().image.url
        except:
            team2_img_url=''
        return team2_img_url
    
class Player(models.Model):
    # id= models.IntegerField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,default=None,limit_choices_to=Q(role__in=["player"])&Q(player__isnull=True))
    matches = models.ManyToManyField(Match,related_name="players",through='MatchPlayerDetails')
    class currentStatus(models.TextChoices):
        INJURED = 'Injured', _('Injured')
        READY = 'Ready to play', _('Ready to play')
        UNKNOWN = 'Unknown', _('Unknown')
    class currentPosition(models.TextChoices):
        ATTACKER = 'Attacker', _('Attacker')
        MIDFIELDER = 'Midfielder', _('Midfielder')
        DEFENDER = 'Defender', _('Defender')
        GOALKEEPER = 'Goalkeeper', _('Goalkeeper')
    
    number = models.IntegerField(choices = [(i,i) for i in range(100)], unique= True, default =0)
    status = models.TextField(choices = currentStatus.choices,default= currentStatus.READY)
    position = models.TextField(choices = currentPosition.choices,default=currentPosition.MIDFIELDER)
    image = models.ImageField(upload_to='player_images/', verbose_name=_("Image"), null=True, blank=True)
    
    def shotRatio(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        scoredShots = matchDetails.aggregate(Sum('shots_on_target'))
        attemptedShots = matchDetails.aggregate(Sum('attempted_shots'))
        return (scoredShots['shots_on_target__sum'] or 0)/(attemptedShots['attempted_shots__sum']+0.001)
    
    def shotConversionRate(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        scoredShots = matchDetails.aggregate(Sum('goals'))
        attemptedShots = matchDetails.aggregate(Sum('shots_on_target'))
        return (scoredShots['goals__sum'] or 0)/(attemptedShots['shots_on_target__sum']+0.001)
    
    def passRatio(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        scoredShots = matchDetails.aggregate(Sum('made_passes'))
        attemptedShots = matchDetails.aggregate(Sum('attempted_passes'))
        return (scoredShots['made_passes__sum'] or 0)/(attemptedShots['attempted_passes__sum']+0.001)
    
    def tackleRatio(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        scoredShots = matchDetails.aggregate(Sum('made_tackles'))
        attemptedShots = matchDetails.aggregate(Sum('attempted_tackles'))
        return (scoredShots['made_tackles__sum'] or 0)/(attemptedShots['attempted_tackles__sum']+0.001)
    
    
    def totalGoals(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        totalGoals = matchDetails.aggregate(Sum('goals'))
        return (totalGoals['goals__sum'] or 0)
    
    def totalPitchTime(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        minutesPlayed = matchDetails.aggregate(Sum('minutes_played'))
        
        hoursPlayed = int((minutesPlayed['minutes_played__sum'] or 0)/60)
        remainingMinutes = mod(minutesPlayed['minutes_played__sum'] or 0, 60)
        return f"{hoursPlayed:02}"+':'+f"{remainingMinutes:02}"
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    def get_absolute_url(self):
        return reverse('player-detail', args = [self.id])
    
class MatchPlayerDetails(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    attempted_shots = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    attempted_passes = models.IntegerField(default=0)
    made_passes = models.IntegerField(default=0)
    attempted_tackles = models.IntegerField(default=0)
    made_tackles = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)

class Ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    ticket_type = models.TextField(default = 'General Admission') # we will have also: VIP, Reserved
    price = models.IntegerField(default = 0)
    quantity = models.IntegerField(default = 0)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default = None,null=True)
class TicketUser(models.Model):  
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE, related_name='ticket')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    account_summary = models.ForeignKey(AccountSummary,on_delete=models.CASCADE,related_name='accountsummary',null=True)
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to=Q(role__in=["admin","journalist"]))
    body = models.TextField()
    image = models.ImageField(upload_to='article_images/', verbose_name=_("Image"), null=True, blank=True,default=None)
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('article-detail', args = [self.id])
class Team(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team_images/', verbose_name=_("Image"), null=True, blank=True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('team-detail', args = [self.id])