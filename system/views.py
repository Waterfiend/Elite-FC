import string
from tkinter import Menu
from django.shortcuts import render,redirect
from django.http import HttpResponse
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from .models import User, Ticket
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

def createTicket(post):
    pass

def createTicketType(post): 
    """TO DO: create functionality to add new ticket type"""
    pass

def deleteTicketType(post):
    """TO DO: create functionality to delete ticket type"""
    pass

def editTicketType(post):
    """TO DO: create functionality to edit ticket type"""
    pass
    
def renderTickets(request):
    """TO DO: create functionality to view ticket types before managing them"""

    buyLinkOptions ={
        'url':'https://images.theconversation.com/files/443350/original/file-20220131-15-1ndq1m6.jpg?ixlib=rb-1.1.0&rect=0%2C0%2C3354%2C2464&q=45&auto=format&w=926&fit=clip',
        'text':'Buy',
        'class':''
    }

    infoLinkOptions ={
        'url':'https://images.theconversation.com/files/443350/original/file-20220131-15-1ndq1m6.jpg?ixlib=rb-1.1.0&rect=0%2C0%2C3354%2C2464&q=45&auto=format&w=926&fit=clip',
        'text':'Details',
        'class':''
    }

    ''' These two should be Ticket attributes not strings'''
    ticketType = 'General Admission'
    ticketNum = '1002'

    buyLink = Component('link',buyLinkOptions).create()  
    infoLink = Component('link',infoLinkOptions).create()  
    
    tableOptions ={
        'table_header':['Ticket Number', 'Ticket Type'],
        'table_rows':[
            [ticketNum, ticketType, infoLink, buyLink]
        ]     
    }
    if (User.role == 'admin'):
        render(request,'system/extras.html')

    form = Component('table',tableOptions).create()
    return render(request,'system/form.html',{'title':'Available Tickets','form':form})