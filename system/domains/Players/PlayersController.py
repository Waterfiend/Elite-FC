from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS
from ...models import User,Match,Player,MatchPlayerDetails
from django.contrib import messages
from helpers.SearchBar import Search
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import re

def renderPlayers(request):
    backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
    backLink = Component('link',backLinkOptions).create()
    tableOptions ={
        'table_header':['Player', 'Rank'],
        'table_rows':[],     
    }
    concatination = {'full_name':['first_name',' ','last_name']}
    (searchBar,users) = Search(request,User,concatination)
    playerUsers = users.filter(role='player') or User.objects.filter(role='player')
    for playerUser in playerUsers:
        playerLinkOptions ={
        'url':'/Matches/'+str(playerUser.id),
        'text':playerUser.first_name+" "+playerUser.last_name,
        'class':''
        }
        playerLink = Component('link', playerLinkOptions).create()
        tableOptions['table_rows'].append([playerLink,playerUser.fan_tier])

    form = Component('table',tableOptions).create()
    return render(request,'system/form.html', {'title':'Players','form':backLink+searchBar+form})
    
def renderPlayerMatches(request,id):
    tableOptions ={
        'table_header':['Match','Attempted Shots', 'Goals','Attempted Passes', "Made Passes", 'Fouls', "Minutes Played"],
        'table_rows':[],     
    }
    
    playerUser = User.objects.filter(id=id).first()
    (player,created) = Player.objects.get_or_create(user=playerUser)
    player = Player.objects.get(user=playerUser)
    print(player.id)
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
    
    match_ids = []
    allMatches = Match.objects.all()
    for match in allMatches:
        match_ids.append("<!--"+str(match.id)+"-->"+match.date+" "+match.time+" "+match.team1+"VS"+match.team2)    
    formOptions = {'form_class':'form','method':'POST','action':'/editStatisticsValidate/'+str(id)+'/'+str(match_id),
        'form_fields':[
            {'label':'Attempted Shots','input_props':{'name':'attempted_shots','type':'number', 'title':'Only numbers allowed', 'value':str(values['attempted_shots'])}},
            {'label':'Goals','input_props':{'name':'goals','type':'number', 'title':'Only numbers allowed','value':str(values['goals'])}},
            {'label':'Attempted Passes','input_props':{'name':'attempted_passes','type':'number', 'title':'Only numbers allowed','value':str(values['attempted_passes'])}},
            {'label':'Made Passes','input_props':{'name':'made_passes','type':'number','title':'Only numbers allowed','value':str(values['made_passes'])}},
            {'label':'Fouls','input_props':{'name':'fouls','type':'number','title':'Only numbers allowed','value':str(values['fouls'])}},
            {'label':'Minutes Played','input_props':{'name':'minutes_played','type':'number','value':str(values['minutes_played'])}},
            {'label':'Match','field_type':'select','input_props':{'name':'match','type':'text','size':'4','selected':playerMatch_id},'select_options': match_ids},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['Attempted Shots_input','Goals_input','Attempted Passes_input','Made Passes_input','Fouls_input', 'Minutes Played_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    backLinkOptions ={
            'url':'/Matches/'+str(id),
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
    backLink = Component('link',backLinkOptions).create()
    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})

def editStatisticsValidate(request,id,match_id):
    if(request.method == 'POST'):
        infoDict = {}
        for key in request.POST:
            infoDict[key]=request.POST[key]
        infoDict.pop('csrfmiddlewaretoken')
        matchInfo = infoDict['match']
        extracted_match_id = re.search(r'<!--(.*?)-->', matchInfo).group(1)
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
    
class PlayerDetailView(DetailView): 
    model = Player
    template_name = 'system/player_details.html'


class AddPlayerView(CreateView):
    model = Player
    template_name = 'system/add_player.html'
    fields = ['user','number','status','position']

class UpdatePlayerView(UpdateView):
    model = Player
    template_name = 'system/update_player.html'
    fields = ['user','number','status','position']

class DeletePlayerView(DeleteView):
    model = Player
    template_name = 'system/delete_player.html'
    success_url = reverse_lazy('playerstat')