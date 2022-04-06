import string
from tkinter import Menu
from django.shortcuts import render,redirect
from django.http import HttpResponse
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from .models import User, Ticket, Match
from django.contrib import messages
import hashlib
# Create your views here.

def hello(request):
    deleteLinkOptions ={
        'url':'https://images.theconversation.com/files/443350/original/file-20220131-15-1ndq1m6.jpg?ixlib=rb-1.1.0&rect=0%2C0%2C3354%2C2464&q=45&auto=format&w=926&fit=clip',
        'text':'delete',
        'class':''
    }
    deleteLink = Component('link',deleteLinkOptions).create()  
    tableOptions ={
        'table_header':['Name', 'Email', 'Edit', 'Delete'],
        'table_rows':[
            ['Hadi','email','ee',deleteLink]
        ]     
    }
    form = Component('table',tableOptions).create()    
    return render(request,'system/form.html',{'title':'Table','form':form})

def renderRegistration(request):

    title = 'Registration Form'
    
    formOptions = {'form_class':'form','method':'POST','action':'/registerValidate/',
        'form_fields':[
            {'label':'First Name','input_props':{'name':'first_name','type':'text', 'pattern':"[A-Za-z]+", 'title':'Only letters allowed'}},
            {'label':'Last Name','input_props':{'name':'last_name','type':'text', 'pattern':"[A-Za-z]+", 'title':'Only letters allowed'}},
            {'label':'Email','input_props':{'name':'email','type':'email', 'placeholder':'email@email.com', 'title':'Email must contain @'}},
            {'label':'Password','input_props':{'name':'password','type':'password'}},
            {'label':'Confirm Password','input_props':{'name':'confirm_password','type':'password'}},
            {'label':'Birth Date','input_props':{'name':'date_of_birth','type':'date'}},
            {'label':'Fan Tier','field_type':'select','input_props':{'name':'fan_tier','type':'text'},'select_options':['Bronze','Silver','Gold','Elite']},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['First Name_input','Last Name_input','Email_input','Password_input','Confirm Password_input', 'Birth Date_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    confirmPasswordValidationScript = ConfirmPasswordErrorJS('Password_input','Confirm Password_input')
    confirmPasswordValidationScriptComponenet = Component('script',confirmPasswordValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet+confirmPasswordValidationScriptComponenet})

def validateRegistration(request):
    if(request.method == 'POST'):
        infoDict = {}
        for key in request.POST:
            infoDict[key]=request.POST[key]
        infoDict.pop('csrfmiddlewaretoken')
        infoDict.pop('confirm_password')
        infoDict['password'] = hashlib.md5(infoDict['password'].encode('utf-8')).hexdigest()
        try:
            existingRecord = User.objects.filter(email=infoDict['email']).first()
        except:
            existingRecord = None
        if(existingRecord is not None):
            messages.error(request,'Email '+ infoDict['email'] +' already exists. Please use a different email')
        else:
            User.objects.create(**infoDict)
            messages.success(request,'Registration Successful')
        return redirect('/register')
    
def renderLogin(request):
    title = 'Login Form'
    
    formOptions = {'form_class':'form','method':'GET','action':'/loginValidate/',
        'form_fields':[
            {'label':'Email','input_props':{'name':'email','type':'email', 'placeholder':'email@email.com', 'title':'Email must contain @'}},
            {'label':'Password','input_props':{'name':'password','type':'password'}},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['Email_input','Password_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet})

def validateLogin(request):
    if(request.method == 'GET'):
        infoDict = request.GET.copy()
        try:
            existingRecord = User.objects.filter(email=infoDict['email'],password=hashlib.md5(infoDict['password'].encode('utf-8')).hexdigest()).first()
        except:
            existingRecord = None
        if(existingRecord is not None):
            messages.success(request,'Login Successful! Welcome '+ existingRecord.first_name)
        else:
            messages.error(request,'Login Failed: Wrong Credentials')

        return redirect('/')

def manageUsers(request):
    pass

def createTicket(request):
    
    title = 'Registration Form'
    matches = Match.objects.all()
    match_ids = []

    for match in matches:
        match_ids.append(str(match.id))

    formOptions = {'form_class':'form','method':'POST','action':'/TicketValidate/',
        'form_fields':[
            {'label':'Quantity','input_props':{'name':'quantity','type':'text', 'pattern':"[0-9]+", 'title':'Only Numbers allowed'}},
            {'label':'Ticket Type','field_type':'select','input_props':{'name':'ticket_type','type':'text'},'select_options':['General Admission', 'VIP', 'Reserved']},
            {'label':'Price','input_props':{'name':'price','type':'text', 'pattern':"[0-9]+", 'title':'Only Numbers allowed'}},
            {'label':'Matches','field_type':'select','input_props':{'name':'match','type':'text'},'select_options': match_ids},

        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['Quantity_input','Ticket Type_input','Price_input','Matches_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()


    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet})

def deleteTicket(request,id):
    existingRecord = Ticket.objects.filter(id=id)
    existingRecord.delete()
    return redirect('/Tickets/')

def validateTicket(request):
    if(request.method == 'POST'):
        infoDict = request.POST.copy() # POST takes all what is in Form from submit
        match = Match.objects.filter(id=infoDict["match"]).first()
        try:
            existingRecord = Ticket.objects.filter(match=match).first() # match of model = match fetched
        except:
            existingRecord = None
        if(existingRecord is None):
            Ticket.objects.create(ticket_type=infoDict["ticket_type"], quantity=infoDict["quantity"], match=match, price = infoDict["price"])
            messages.success(request,'Ticket Successfully Added')
        else:
            messages.error(request,'Ticket for already existing match')

        return redirect('/Tickets/')

def renderTickets(request):

    addOptions = {
        'url':'/CreateTicketForm/',
        'text':'Add Ticket',
        'class':''
    }
    addLink = Component('link', addOptions).create()

    tableOptions ={
        'table_header':['Ticket Number', 'Match Date', "Ticket Type", "Price", "Quantity"],
        'table_rows':[],     
    }
    tickets = Ticket.objects.all()
    for ticket in tickets:
        deleteLinkOptions ={
        'url':'/deleteTicket/'+str(ticket.id),
        'text':'Delete',
        'class':''
        }
        editLinkOptions ={
        'url':'/editTicket/'+str(ticket.id),
        'text':'Edit',
        'class':''
        }
        editLink = Component('link', editLinkOptions).create()
        deleteLink = Component('link', deleteLinkOptions).create()
        tableOptions['table_rows'].append([str(ticket.id), ticket.match.date, ticket.ticket_type, str(ticket.price), str(ticket.quantity), deleteLink, editLink])

    form = Component('table',tableOptions).create()
    return render(request,'system/form.html', {'title':'Available Tickets','form':form + addLink})

def editTicket(request,id):
    
    matches = Match.objects.all()
    match_ids = []

    for match in matches:
        match_ids.append(str(match.id))
    
    formOptions = {'form_class':'form','method':'POST','action':'/editTicketValidate/',
        'form_fields':[
            {'label':'Quantity','input_props':{'name':'quantity','type':'text', 'pattern':"[0-9]+", 'title':'Only Numbers allowed'}},
            {'label':'Ticket Type','field_type':'select','input_props':{'name':'ticket_type','type':'text'},'select_options':['General Admission', 'VIP', 'Reserved']},
            {'label':'Price','input_props':{'name':'price','type':'text', 'pattern':"[0-9]+", 'title':'Only Numbers allowed'}},
            {'label':'Matches','field_type':'select','input_props':{'name':'match','type':'text'},'select_options': match_ids},
        ]}
    form = Component('form',formOptions).create(request)

    tickets = Ticket.objects.all()
    for ticket in tickets:
        deleteLinkOptions ={
        'url':'/deleteTicket/'+str(ticket.id),
        'text':'Delete',
        'class':''
        }
        editLinkOptions ={
        'url':'/editTicket/'+str(ticket.id),
        'text':'Edit',
        'class':''
        }
        editLink = Component('link', editLinkOptions).create()

    existingRecord = Ticket.objects.filter(id=id)
    existingRecord.update()
    return render(request,'system/form.html', {'title':'Edit Ticket ' + str(ticket.id),'form':form})

def editTicketValidate(request, id = 0):

    existingRecord = Ticket.objects.filter(id=id)
    if(request.method == 'POST'):
        infoDict = request.POST.copy() # POST takes all what is in Form from submit
        match = Match.objects.filter(id=infoDict["match"]).first()
        try:
            existingRecord = Ticket.objects.filter(match=match).first() # match of model = match fetched
        except:
            existingRecord = None
        if(existingRecord is None):
            Ticket.objects.update(ticket_type=infoDict["ticket_type"], quantity=infoDict["quantity"], match=match, price = infoDict["price"])
            messages.success(request,'Ticket Successfully Edited')
        else:
            messages.error(request,'Invalid Ticket Edit')

        return redirect('/Tickets/')

def renderShop(request):

    tableOptions ={
        'table_header':['Ticket Number', 'Match Date', "Ticket Type", "Price", "Quantity"],
        'table_rows':[],     
    }
    tickets = Ticket.objects.all()
    for ticket in tickets:
        editLinkOptions ={
        'url':'/buyTicket/'+str(ticket.id),
        'text':'Buy',
        'class':''
        }
        editLink = Component('link', editLinkOptions).create()
        tableOptions['table_rows'].append([str(ticket.id), ticket.match.date, ticket.ticket_type, str(ticket.price), str(ticket.quantity), editLink])

    form = Component('table',tableOptions).create()
    return render(request,'system/form.html', {'title':'Available Tickets','form':form})

def buyTicket(request, id = 0):
    
    title = 'Purchase Form'
    tickets = Ticket.objects.all()
    ticket_ids = []

    for ticket in tickets:
        ticket_ids.append(str(ticket.id))

    formOptions = {'form_class':'form','method':'POST','action':'/TicketValidate/',
        'form_fields':[
            {'label':'Confirmation','field_type':'select','input_props':{'name':'ticket_type','type':'text'},'select_options':['Yes', 'No']},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['Quantity_input','Ticket Type_input','Price_input','Matches_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()

    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet})

def purchases(request):

    tableOptions ={
        'table_header':['Ticket Number', 'Match Date', "Ticket Type"],
        'table_rows':[],     
    }
    form = Component('table',tableOptions).create()
    return render(request, 'system/form.html', {'title':'Purchases Tickets','form':form})