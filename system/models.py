from email.policy import default
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from operator import mod

''' ckeditor is a rich text editor with alot of functionalities such as inserting images, 
tables, changing text color and font etc. It will be used to write professional articles for the website'''
from ckeditor.fields import RichTextField 

# Create your models here.
'''
Role model used to define all the available roles on the system
'''
class Role(models.Model):
    id= models.IntegerField(primary_key=True)
    role = models.TextField(default='fan')
'''
Tier model used to define the tiers available
'''
class Tier(models.Model):
    id= models.IntegerField(primary_key=True)
    fan_tier = models.TextField(default='fan')
'''
Permission model used to give permission to a specific role to access a path
'''
class Permission(models.Model):
    id= models.IntegerField(primary_key=True)
    role = models.TextField(default='fan')
    path = models.TextField(default='/')
'''
User model used to define the user information
'''
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    date_of_birth = models.TextField()
    fan_tier = models.TextField()
    role = models.TextField(default='fan')
    
    #the user's full name is retuned whenever we print a user instance
    def __str__(self):
        return self.first_name + ' ' + self.last_name
'''
Salary model used to define the monthly salaries/fees for each tier of every role.
eg. Elite player gets $4000 per month while bronze player gets only $2000
    elite fan pays $50 while bronze fans pay $0
'''
class Salary(models.Model):
     id= models.IntegerField(primary_key=True)
     fan_tier = models.TextField()
     role = models.TextField()
     salary = models.IntegerField(default=0)
'''
AccountSummary model used to define every financial transaction a user makes
'''
class AccountSummary(models.Model):
    # id = models.IntegerField(primary_key=True)
    transaction_name = models.TextField(default="")
    transaction_amount = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    date = models.TextField(default="")

'''
FieldReservation model used to define the field reservation dates and times taken by a certain user
'''
class FieldReservation(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.TextField()
    slot_time = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    account_summary = models.ForeignKey(AccountSummary,on_delete=models.CASCADE,null=True)
'''
Discounts model used to define the discounts each tier benifits from
'''
class Discounts(models.Model):
    id = models.IntegerField(primary_key=True)
    fan_tier = models.TextField()
    discount = models.IntegerField(default=0)
class FanTierFee(models.Model):
    id = models.IntegerField(primary_key=True)
    fan_tier = models.TextField()
    fee = models.IntegerField(default=0)

'''
Match model used to define all the details about a scheduled soccer match
'''
class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.TextField(default = "XX/XX/XX")
    time = models.TextField(default = "XX:XX")
    team1 = models.TextField(default = "")
    team2 = models.TextField(default = "")
    score1 = models.IntegerField(default = 0)
    score2 = models.IntegerField(default = 0)
    location = models.TextField(default="")
    
    # get the url of the team1 logo if it exists and return an empty string otherwise
    def team1Img(self):
        try:
            team1_img_url = Team.objects.filter(name=self.team1).first().image.url
        except:
            team1_img_url=''
        return team1_img_url
    # get the url of the team2 logo if it exists and return an empty string otherwise
    def team2Img(self):
        try:
            team2_img_url = Team.objects.filter(name=self.team2).first().image.url
        except:
            team2_img_url=''
        return team2_img_url

'''
Player model used to define details of a player.
Each player is associated with a user and has many matches which they participated in
A player also has a number, position, status, and profile image
'''
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
    
    # return the ratio of shots on target to total shots for a player instance
    def shotRatio(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        scoredShots = matchDetails.aggregate(Sum('shots_on_target'))
        attemptedShots = matchDetails.aggregate(Sum('attempted_shots'))
        return (scoredShots['shots_on_target__sum'] or 0)/((attemptedShots['attempted_shots__sum'] or 0)+0.001)
    
    # return the percentage og shots on target that resulted in a goal
    def shotConversionRate(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        scoredShots = matchDetails.aggregate(Sum('goals'))
        attemptedShots = matchDetails.aggregate(Sum('shots_on_target'))
        return (scoredShots['goals__sum'] or 0)/((attemptedShots['shots_on_target__sum'] or 0)+0.001)
    
    # return the percentage of passes that are successful
    def passRatio(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        scoredShots = matchDetails.aggregate(Sum('made_passes'))
        attemptedShots = matchDetails.aggregate(Sum('attempted_passes'))
        return (scoredShots['made_passes__sum'] or 0)/((attemptedShots['attempted_passes__sum'] or 0)+0.001)
    
    # return the percentage of tackles that are successful
    def tackleRatio(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        scoredShots = matchDetails.aggregate(Sum('made_tackles'))
        attemptedShots = matchDetails.aggregate(Sum('attempted_tackles'))
        return (scoredShots['made_tackles__sum'] or 0)/((attemptedShots['attempted_tackles__sum'] or 0)+0.001)
    
    # return the total carear goals
    def totalGoals(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        totalGoals = matchDetails.aggregate(Sum('goals'))
        return (totalGoals['goals__sum'] or 0)
    
    # return the time spent on the field
    def totalPitchTime(self):
        matchDetails = MatchPlayerDetails.objects.filter(player=self)
        minutesPlayed = matchDetails.aggregate(Sum('minutes_played'))
        
        hoursPlayed = int((minutesPlayed['minutes_played__sum'] or 0)/60)
        remainingMinutes = mod(minutesPlayed['minutes_played__sum'] or 0, 60)
        return f"{hoursPlayed:02}"+':'+f"{remainingMinutes:02}"
    
    def getMatchStatistics(self):
        matches = MatchPlayerDetails.objects.filter(player=self)
        return matches
        
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    def get_absolute_url(self):
        return reverse('player-detail', args = [self.id])

'''
MatchPlayerDetails is the through table that stores the statistics for every match a player participated in
'''    
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

'''
Ticket model is used to define the information about a ticket being sold including the price, quantity available, and the match accissabe using this ticket
'''
class Ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    ticket_type = models.TextField(default = 'General Admission') # we will have also: VIP, Reserved
    price = models.IntegerField(default = 0)
    quantity = models.IntegerField(default = 0)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default = None,null=True)

'''
TicketUser model a through table used to associate every purchaced ticket with a user
'''
class TicketUser(models.Model):  
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE, related_name='ticket')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    account_summary = models.ForeignKey(AccountSummary,on_delete=models.CASCADE,related_name='accountsummary',null=True)

'''
TicketUser model is used to define the details of news article
'''
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to=Q(role__in=["admin","journalist"])) # only admins and journalists can be authors of articles
    image = models.ImageField(upload_to='article_images/', verbose_name=_("Image"), null=True, blank=True,default=None)
    # body = models.TextField()
    body = RichTextField(blank=True, null=True)# RichTextField from ckeditor is used to define the body of the article 

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('article-detail', args = [self.id])
'''
TicketUser model is used to define the details of teams
'''
class Team(models.Model):
    name = models.CharField(max_length=255,unique= True)
    image = models.ImageField(upload_to='team_images/', verbose_name=_("Image"), null=True, blank=True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('team-detail', args = [self.id])