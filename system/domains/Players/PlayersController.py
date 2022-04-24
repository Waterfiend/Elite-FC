from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS,FormValidateSumJS
from ...models import User,Match,Player,MatchPlayerDetails
from django.contrib import messages
from helpers.SearchBar import Search
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import re
'''
renderPlayers function renders the players in a table form for the player match statistics page
'''
def renderPlayers(request):
    backLinkOptions ={# define a back buttton
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
    backLink = Component('link',backLinkOptions).create()# create the back button
    tableOptions ={# define the player table
        'table_header':['Player', 'Rank'],
        'table_rows':[],     
    }
    
    # use the Search function to create a new instance of the search filter and return a filtered set of users based on the user input in the search bar
    concatination = {'full_name':['first_name',' ','last_name']}# define a concatination of full name from first and last names
    (searchBar,users) = Search(request,User,concatination)
    playerUsers = users.exclude(player__isnull=True) or User.objects.exclude(player__isnull=True)

    for playerUser in playerUsers: # for each player user 
        playerLinkOptions ={ # define a link that takes us to the player user's matches
        'url':'/Matches/'+str(playerUser.id),
        'text':playerUser.first_name+" "+playerUser.last_name,
        'class':''
        }
        playerLink = Component('link', playerLinkOptions).create()# create the link
        tableOptions['table_rows'].append([playerLink,playerUser.fan_tier])# add the player user into the player table

    table = Component('table',tableOptions).create()
    return render(request,'system/form.html', {'title':'Players','form':backLink+searchBar+table})
'''
renderPlayerMatches function renders the match statistics table for each player
it is built very similarly to renderPlayers
each match has its statistics, edit button, and delete button
there is also an add button to add new match statistics for the player
'''  
def renderPlayerMatches(request,id):
    tableOptions ={
        'table_header':['Match','Attempted Shots', 'Goals','Attempted Passes', "Made Passes", 'Fouls', "Minutes Played"],
        'table_rows':[],     
    }
    
    playerUser = User.objects.filter(id=id).first()
    (player,created) = Player.objects.get_or_create(user=playerUser)
    player = Player.objects.get(user=playerUser)
    playerMatches = player.matches.all()
    print(playerMatches)
    for match in playerMatches:
        matchDetails=MatchPlayerDetails.objects.filter(player=player,match=match).first()
        editLinkOptions ={
        'url':'/playerStatisticsForm/'+str(playerUser.id)+'/'+str(match.id),
        'text':'Edit',
        'class':'btn btn-success'
        }
        editLink = Component('link', editLinkOptions).create()
        deleteLinkOptions ={
        'url':'/deleteStatistics/'+str(playerUser.id)+'/'+str(match.id),
        'text':'Delete',
        'class':'btn btn-danger'
        }
        deleteLink = Component('link', deleteLinkOptions).create()
        matchInfo = match.date+" "+match.time+" "+match.team1+"VS"+match.team2
        tableOptions['table_rows'].append([matchInfo,str(matchDetails.attempted_shots),str(matchDetails.goals),str(matchDetails.attempted_passes),str(matchDetails.made_passes),str(matchDetails.fouls),str(matchDetails.minutes_played),editLink,deleteLink])
    addLinkOptions ={
            'url':'/playerStatisticsForm/'+str(playerUser.id)+'/'+str(0),
            'text':'Add Match Statistic',
            'class':'btn btn-success'
        }
    addLink = Component('link',addLinkOptions).create() 
    backLinkOptions ={
            'url':'/Players/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
    backLink = Component('link',backLinkOptions).create()
    form = Component('table',tableOptions).create()
    return render(request,'system/form.html', {'title':playerUser.first_name+"'s Statistics",'form':backLink+addLink+form})
'''
playerStatisticsForm creates the form that should be filled by the user to create or edot a match statistic
when match_id = 0 we are in creation mode, else we edit the match statistic whith the given id.
'''
def playerStatisticsForm(request,id=0,match_id=0):
    if match_id != 0:
        existingUser = User.objects.filter(id=id).first()
        player = Player.objects.filter(user=existingUser).first()
        playerMatch = player.matches.filter(id=match_id).first()
        matchStatistic = MatchPlayerDetails.objects.filter(player=player,match=playerMatch).first()
        title = 'Edit Match Statistic'
        values = matchStatistic.__dict__
        playerMatch_id = "<!--"+str(playerMatch.id)+"-->"+playerMatch.date+" "+playerMatch.time+" "+playerMatch.team1+"VS"+playerMatch.team2

    else:
        title = 'Add Match Statistic'
        values = {field.name:'' for field in MatchPlayerDetails._meta.fields}
        playerMatch_id = ''
    
    #create match list in the desired format from matches
    match_ids = []
    allMatches = Match.objects.all()
    for match in allMatches:
        match_ids.append("<!--"+str(match.id)+"-->"+match.date+" "+match.time+" "+match.team1+"VS"+match.team2)    
    # define the match statistics form
    formOptions = {'form_class':'form','method':'POST','action':'/editStatisticsValidate/'+str(id)+'/'+str(match_id),
        'form_fields':[
            {'label':'Attempted Shots','input_props':{'name':'attempted_shots','type':'number', 'title':'Only numbers allowed', 'min':'0','value':str(values['attempted_shots'])}},
            {'label':'Shots On Target','input_props':{'name':'shots_on_target','type':'number', 'title':'Only numbers allowed', 'min':'0','value':str(values['shots_on_target'])}},
            {'label':'Goals','input_props':{'name':'goals','type':'number', 'title':'Only numbers allowed','min':'0','value':str(values['goals'])}},
            {'label':'Attempted Passes','input_props':{'name':'attempted_passes','type':'number', 'title':'Only numbers allowed','min':'0','value':str(values['attempted_passes'])}},
            {'label':'Successful Passes','input_props':{'name':'made_passes','type':'number','title':'Only numbers allowed','min':'0','value':str(values['made_passes'])}},
            {'label':'Attempted Tackles','input_props':{'name':'attempted_tackles','type':'number', 'title':'Only numbers allowed','min':'0','value':str(values['made_tackles'])}},
            {'label':'Successful Tackles','input_props':{'name':'made_tackles','type':'number','title':'Only numbers allowed','min':'0','value':str(values['made_tackles'])}},
            {'label':'Fouls','input_props':{'name':'fouls','type':'number','title':'Only numbers allowed','min':'0','value':str(values['fouls'])}},
            {'label':'Minutes Played','input_props':{'name':'minutes_played','type':'number','min':'0','value':str(values['minutes_played'])}},
            {'label':'Match','field_type':'select','input_props':{'name':'match','type':'text','size':'4','selected':playerMatch_id},'select_options': match_ids},
        ]}
    form = Component('form',formOptions).create(request)# create the match statistic form
    
    # this JavaScript is used render the validation errors that result when the user fills a field with incorrectly formatted data   
    formValidationScript = FormValidationErrorsJS(['Attempted Shots_input','Goals_input','Shots On Target_input','Attempted Passes_input','Successful Passes_input','Attempted Tackles_input','Successful Tackles_input','Fouls_input', 'Minutes Played_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()#create script componenet
    
    # this JavaScript varifies that the shots on target never exceed the attempted shots
    shotsSumValidation = FormValidateSumJS('Attempted Shots_input',['Shots On Target_input'])
    shotsSumValidationScriptComponenet = Component('script',shotsSumValidation).create()#create script componenet
    
    # this JavaScript varifies that the goals never exceed the shots on target
    goalsSumValidation = FormValidateSumJS('Shots On Target_input',['Goals_input'])
    goalsSumValidationScriptComponenet = Component('script',goalsSumValidation).create()#create script componenet
    
    # this JavaScript varifies that the passes on target never exceed the attempted passes
    passesSumValidation = FormValidateSumJS('Attempted Passes_input',['Successful Passes_input'])
    passesSumValidationScriptComponenet = Component('script',passesSumValidation).create()#create script componenet
    
    # this JavaScript varifies that the tackles on target never exceed the attempted tackles
    tacklesSumValidation = FormValidateSumJS('Attempted Tackles_input',['Successful Tackles_input'])
    tacklesSumValidationScriptComponenet = Component('script',tacklesSumValidation).create()#create script componenet
    
    # aggregate all the script componenets
    jsScripts = formValidationScriptComponenet+shotsSumValidationScriptComponenet+goalsSumValidationScriptComponenet+passesSumValidationScriptComponenet+tacklesSumValidationScriptComponenet
    
    backLinkOptions ={
            'url':'/Matches/'+str(id),
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
    backLink = Component('link',backLinkOptions).create()
    return render(request,'system/form.html',{'title':title,'form':backLink+form+jsScripts})
'''
editStatisticsValidate function validates the statistic before commiting to database.
check that the match is not already present in the database
'''
def editStatisticsValidate(request,id,match_id):
    if(request.method == 'POST'):
        infoDict = {}
        for key in request.POST:
            infoDict[key]=request.POST[key]
        infoDict.pop('csrfmiddlewaretoken')
        matchInfo = infoDict['match']
        extracted_match_id = re.search(r'<!--(.*?)-->', matchInfo).group(1) # regular expressions to extract the match id from the match info
        match = Match.objects.filter(id=extracted_match_id).first()
        user = User.objects.filter(id=id).first()
        player = Player.objects.filter(user=user).first()
        
        infoDict['player'] = player
        infoDict['match'] = match
        
        print(player,match)
        
        try:
            matchStatistic = MatchPlayerDetails.objects.filter(player=player,match=match).first()
        except:
            matchStatistic = None
        
        if(matchStatistic is not None and matchStatistic.match.id!=match_id):
            messages.error(request,'Statistics for this player on this match already exist')
        else:
            if match_id !=0:
                matchStatistic.__dict__.update(infoDict)
                matchStatistic.save()
                messages.success(request,'Update Successful')
            else:
                MatchPlayerDetails.objects.create(**infoDict)
                messages.success(request,'Add Successful')
        return redirect('/Matches/'+str(id))
    
def deleteStatistics(request,id,match_id):
    existingRecord = MatchPlayerDetails.objects.filter(player__user__id=id,match__id=match_id)
    existingRecord.delete()
    return redirect('/Matches/'+str(id))


class HomeView(ListView):
    model = Player
    template_name = 'system/playerstat.html'

class FrontHomeView(ListView):
    model = Player
    template_name = 'system/playerstat_front.html'


class PlayerDetailView(DetailView): 
    model = Player
    template_name = 'system/player_details.html'
    
class playerstatisticsFront(DetailView):
    model = Player
    template_name = 'system/player_details_front.html'
    
class AddPlayerView(CreateView):
    model = Player
    template_name = 'system/add_player.html'
    fields = ['user','number','status','position','image']

class UpdatePlayerView(UpdateView):
    model = Player
    template_name = 'system/update_player.html'
    fields = ['number','status','position','image']

class DeletePlayerView(DeleteView):
    model = Player
    template_name = 'system/delete_player.html'
    success_url = reverse_lazy('playerstat')