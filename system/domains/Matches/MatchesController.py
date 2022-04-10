from django.contrib import messages
from django.shortcuts import render, redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS
from ...models import Match
from helpers.SearchBar import Search
"""
Displays the schedule of the playing teams.
"""
def display_schedule(request):
    concatination = {}
    (searchBar,matches) = Search(request,Match,concatination)
    matches = matches or Match.objects.all()
    addLinkOptions = {
        'url': '/editmatch/' + str(0),
        'text': 'Add Match',
        'class': 'btn btn-success'
    }
    addLink = Component('link', addLinkOptions).create()
    backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
    }
    backLink = Component('link',backLinkOptions).create()
    table_options = {
        'table_header': ['Team 1', 'Team 2', 'Score', 'Location', 'Date', 'Edit', 'Delete'],
        # Note these are examples of a generic schedule until they are stored in the database
        'table_rows': [
        ]
    }
    for match in matches:
        edit_link_option = {
            'url': '/editmatch/' + str(match.id),
            'text': 'edit',
            'class': 'btn btn-success'
        }
        edit_link = Component('link', edit_link_option).create()
        delete_link_option = {
            'url': '/deletematch/' + str(match.id),
            'text': 'delete',
            'class': 'btn btn-danger'
        }
        delete_link = Component('link', delete_link_option).create()
        table_options['table_rows'].append(
            [match.team1, match.team2, str(match.score1) + "-" + str(match.score2), match.location, match.date, edit_link, delete_link])
    form = Component('table', table_options).create()
    return render(request, 'system/form.html', {'title': 'Matches', 'form': backLink+addLink+searchBar+form})


def delete_match(request, match_id):
    existing_match = Match.objects.filter(id=match_id)
    existing_match.delete()
    return redirect('/schedule')


"""
    date = models.TextField(default="XX/XX/XX")
    time = models.TextField(default="XX:XX")
    team1 = models.TextField(default="")
    team2 = models.TextField(default="")
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    location = models.TextField(default="")
"""


def display_matchform(request, match_id=0):
    backLinkOptions ={
            'url':'/schedule/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
    }
    backLink = Component('link',backLinkOptions).create()
    if match_id != 0:
        existing_match = Match.objects.filter(id=match_id).first()
        title = 'Edit ' + existing_match.team1 + ' VS. ' + existing_match.team2
        values = existing_match.__dict__
    else:
        title = 'Add Match'
        values = {field.name: '' for field in Match._meta.fields}
    formOptions = {'form_class': 'form', 'method': 'POST', 'action': '/postmatch/' + str(match_id),
                       'form_fields': [
                           {'label': 'Team 1',
                            'input_props': {'name': 'team1', 'type': 'text', 'pattern': "[A-Za-z]+",
                                            'title': 'Only letters allowed', 'value': values['team1']}},
                           {'label': 'Team 2',
                            'input_props': {'name': 'team2', 'type': 'text', 'pattern': "[A-Za-z]+",
                                            'title': 'Only letters allowed', 'value': values['team2']}},
                           {'label': 'Date',
                            'input_props': {'name': 'date', 'type': 'date', 'value': values['date']}},
                           {'label': 'Time', 'input_props': {'name': 'time', 'type': 'time','value': values['time']}},
                           {'label': 'Location',
                            'input_props': {'name': 'location', 'type': 'text','value': values['location']}},
                           {'label': 'Score (Team 1)',
                            'input_props': {'name': 'score1', 'type': 'text', 'pattern': "[0-9]+",
                                            'title': 'Only numbers allowed', 'value': str(values['score1'])}},
                           {'label': 'Score (Team 2)',
                            'input_props': {'name': 'score2', 'type': 'text', 'pattern': "[0-9]+",
                                            'title': 'Only numbers allowed', 'value': str(values['score2'])}},
                       ]}
    form = Component('form', formOptions).create(request)
    formValidationScript = FormValidationErrorsJS(
        ['Team 1_input', 'Team 2_input', 'Date_input', 'Time_input', 'Location_input', 'Score (Team 1)_input',
         'Score (Team 2)_input'])
    formValidationScriptComponent = Component('script', formValidationScript).create()
    return render(request, 'system/form.html', {'title': title, 'form': backLink+form + formValidationScriptComponent})


def post_match(request, match_id):
    if request.method == 'POST':
        infoDict = {}
        for key in request.POST:
            infoDict[key] = request.POST[key]
        infoDict.pop('csrfmiddlewaretoken')
        try:
            existingRecord = Match.objects.filter(id=match_id).first()
        except:
            existingRecord = None
        if match_id != 0:
            existingRecord.__dict__.update(infoDict)
            existingRecord.save()
            messages.success(request, 'Update Successful')
        else:
            Match.objects.create(**infoDict)
            messages.success(request, 'Add Successful')
        return redirect('/schedule')
