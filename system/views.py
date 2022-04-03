from turtle import title
from django.shortcuts import render,redirect
from django.http import HttpResponse
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from .models import Permission, User,FieldReservation,AccountSummary,Discounts,Ticket,Match,Role,Tier
from django.contrib import messages
import hashlib
from datetime import datetime
import re
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



def accountSummary(request):
    if 'login' in request.session:
        title= 'Account Summary'
        user = User.objects.filter(email=request.session['login']['email']).first()
        accountDetails = AccountSummary.objects.filter(user = user).all()
        tableOptions ={
                'table_header':['Transaction Name', 'Transaction Amount ($)'],
                'table_rows':[
                ]     
            }
         
        for deatail in accountDetails:  
            tableOptions['table_rows'].append([deatail.transaction_name,str(deatail.transaction_amount)])
        table = Component('table',tableOptions).create() 
        return render(request,'system/form.html',{'title':title,'form':table})   
    else:
        messages.error(request,'You must Login to Reserve the Field')
        return redirect('/')
