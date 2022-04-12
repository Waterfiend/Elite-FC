from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS
from ...models import User,Ticket,Match,AccountSummary,Discounts
from django.contrib import messages
import re


def createTicket(request):
    
    title = 'Add Ticket'
    matches = Match.objects.all()
    match_ids = []
    backLinkOptions ={
            'url':'/Tickets/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
    backLink = Component('link',backLinkOptions).create()
    for match in matches:
        match_ids.append("<!--"+str(match.id)+"-->"+match.date+" "+match.time+" "+match.team1+"VS"+match.team2)

    formOptions = {'form_class':'form','method':'POST','action':'/TicketValidate/',
        'form_fields':[
            {'label':'Quantity','input_props':{'name':'quantity','type':'text', 'pattern':"[0-9]+", 'title':'Only Numbers allowed'}},
            {'label':'Ticket Type','field_type':'select','input_props':{'name':'ticket_type','type':'text'},'select_options':['General Admission', 'VIP', 'Reserved']},
            {'label':'Price','input_props':{'name':'price','type':'text', 'pattern':"[0-9]+", 'title':'Only Numbers allowed'}},
            {'label':'Match','field_type':'select','input_props':{'name':'match','type':'text','size':'4'},'select_options': match_ids},

        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['Quantity_input','Ticket Type_input','Price_input','Match_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()


    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})

def deleteTicket(request,id):
    existingRecord = Ticket.objects.filter(id=id).first()
    matchTeams = existingRecord.match.team1 +' VS '+existingRecord.match.team2
    AccountSummary.objects.filter(transaction_name="Ticket "+ matchTeams +" "+existingRecord.ticket_type+" " + existingRecord.match.date).delete()
    existingRecord.delete()
    return redirect('/Tickets/')

def validateTicket(request):
    if(request.method == 'POST'):
        infoDict = request.POST.copy() # POST takes all what is in Form from submit
        matchInfo = infoDict['match']
        id = re.search(r'<!--(.*?)-->', matchInfo).group(1)
        match = Match.objects.filter(id=id).first()
        try:
            existingRecord = Ticket.objects.filter(match=match,ticket_type=infoDict["ticket_type"]).first() # match of model = match fetched
        except:
            existingRecord = None
        if(existingRecord is None):
            Ticket.objects.create(ticket_type=infoDict["ticket_type"], quantity=infoDict["quantity"], match=match, price = infoDict["price"])
            messages.success(request,'Ticket Successfully Added')
        else:
            messages.error(request,'Ticket for already existing match')

        return redirect('/Tickets/')

def renderTickets(request):
    if 'login' in request.session:
        user = User.objects.filter(email=request.session['login']['email']).first()
        if user.role in ['admin','staff']:
            addOptions = {
                'url':'/CreateTicketForm/',
                'text':'Add Ticket',
                'class':'btn btn-success'
            }
            addLink = Component('link', addOptions).create()
            backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
            backLink = Component('link',backLinkOptions).create()
            tableOptions ={
                'table_header':['Ticket Number', 'Match Date', "Ticket Type", "Price", "Quantity"],
                'table_rows':[],     
            }
            tickets = Ticket.objects.all()
            for ticket in tickets:
                deleteLinkOptions ={
                'url':'/deleteTicket/'+str(ticket.id),
                'text':'Delete',
                'class':'btn btn-danger'
                }
                editLinkOptions ={
                'url':'/editTicket/'+str(ticket.id),
                'text':'Edit',
                'class':'btn btn-success'
                }
                editLink = Component('link', editLinkOptions).create()
                deleteLink = Component('link', deleteLinkOptions).create()
                tableOptions['table_rows'].append([str(ticket.id), ticket.match.date, ticket.ticket_type, str(ticket.price), str(ticket.quantity), deleteLink, editLink])

            form = Component('table',tableOptions).create()
            return render(request,'system/form.html', {'title':'Available Tickets','form':backLink+addLink+form })
        else:
            messages.error(request,'Unauthorized Access')
            return redirect('/')
    else:
        messages.error(request,'You must Login to manage tickets')
        return redirect('/')
def editTicket(request,id):
    backLinkOptions ={
            'url':'/Tickets/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
    backLink = Component('link',backLinkOptions).create()
    matches = Match.objects.all()
    match_ids = []

    for match in matches:
        match_ids.append(str(match.id))
    existingRecord = Ticket.objects.filter(id=id).first()
    formOptions = {'form_class':'form','method':'POST','action':'/editTicketValidate/',
        'form_fields':[
            {'label':'Quantity','input_props':{'name':'quantity','type':'text', 'pattern':"[0-9]+", 'title':'Only Numbers allowed','value':str(existingRecord.quantity)}},
            {'label':'Price','input_props':{'name':'price','type':'text', 'pattern':"[0-9]+", 'title':'Only Numbers allowed','value':str(existingRecord.price)}},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['Quantity_input','Ticket Type_input','Price_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    return render(request,'system/form.html', {'title':'Edit Ticket','form':backLink+form+formValidationScriptComponenet})

def editTicketValidate(request, id = 0):

    existingRecord = Ticket.objects.filter(id=id)
    if(request.method == 'POST'):
        infoDict = request.POST.copy() # POST takes all what is in Form from submit
        # match = Match.objects.filter(id=infoDict["match"]).first()
        # try:
        #     existingRecord = Ticket.objects.filter(match=match).first() # match of model = match fetched
        # except:
        #     existingRecord = None
        # if (existingRecord is  None) or (existingRecord is not None):
        Ticket.objects.update(quantity=infoDict["quantity"], price=infoDict["price"])
        messages.success(request,'Ticket Successfully Edited')
        # else:
        #     messages.error(request,'Invalid Ticket Edit')

        return redirect('/Tickets/')
def ticketsShop(request):
    tableOptions ={
                'table_header':['Match Teams', 'Match Date', "Ticket Type", "Quantity Available", "Price"],
                'table_rows':[],     
            }
    tickets = Ticket.objects.all()
    user = User.objects.filter(email=request.session['login']['email']).first()
    discount = Discounts.objects.filter(fan_tier=user.fan_tier).first()
    for ticket in tickets:
        buyLinkOptions ={
            'url':'/buyTicket/'+str(ticket.id),
            'text':'Buy',
            'class':'btn btn-dark'
        }
        buyLink = Component('link',buyLinkOptions).create()
        matchTeams = ticket.match.team1 +' VS '+ticket.match.team2
        totalCharge = ticket.price*(100-discount.discount)/100
        tableOptions['table_rows'].append([matchTeams,ticket.match.date, ticket.ticket_type,  str(ticket.quantity), '<del>'+str(ticket.price)+'</del>'+' <span style="color:red">'+str(totalCharge)+'<span>' + '<span style="color:grey">'+' Save '+ str(discount.discount) +'% as '+ user.fan_tier +' tier'+'<span>',buyLink])

    form = Component('table',tableOptions).create()
    return render(request,'system/form.html', {'title':'Available Tickets','form':form })
def buyTicket(request,id):
    ticket = Ticket.objects.filter(id=id).first()
    user = User.objects.filter(email=request.session['login']['email']).first()
    discount = Discounts.objects.filter(fan_tier=user.fan_tier).first()
    totalCharge = ticket.price*(100-discount.discount)/100
    if(ticket.quantity > 0):
        ticket.quantity = ticket.quantity -1
        ticket.save()
        matchTeams = ticket.match.team1 +' VS '+ticket.match.team2
        AccountSummary.objects.create(user=user,transaction_name="Ticket "+ matchTeams +" "+ticket.ticket_type+" "+ ticket.match.date,transaction_amount=totalCharge)
        messages.success(request,'Ticket Purchace Successfully')
    else:
        messages.error(request,'Ticket Sold Out')
    return redirect('/ticketsShop/')