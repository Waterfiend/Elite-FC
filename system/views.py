from calendar import calendar
import hashlib

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from .models import Permission, User,FieldReservation,AccountSummary,Discounts,Ticket,Match,Role,Tier
from django.contrib import messages
import hashlib
from datetime import datetime
import re
from .helpers.Calendar import Calendar
from django.db.models import Max
# Create your views here.
def carousel():
    return Component('container',{'type':'div',
                           'content':
        ''''''}).create()
def hello(request):
    today = datetime.today().strftime('%Y-%m-%d')
    todaySplit = today.split('-')
    year = int(todaySplit[0])
    month = int(todaySplit[1])
    def eventAccess(event):
        return event.team1+' VS '+event.team2
    cal = Calendar(year,month,Match,eventAccess)
    
    latest_result = Match.objects.filter(date__lt=today).order_by('-date').first()
    if latest_result:
        team1_header = Component('container',{"type":'h4','content':latest_result.team1}).create()
        team2_header = Component('container',{"type":'h4','content':latest_result.team2}).create()
        VS_header = Component('container',{"type":'h2','content':'VS'}).create()
        score1_header = Component('container',{"type":'h5','content':str(latest_result.score1)}).create()
        score2_header = Component('container',{"type":'h5','content':str(latest_result.score2)}).create()
        latest_result_html = Component('table',{"table_class":'latest_result',
                                    'table_rows':[[team1_header,VS_header,team2_header],
                                                  [score1_header,"",score2_header],
                                                  ['',latest_result.location+' '+latest_result.date+' '+latest_result.time,''],
                                                   ]        
                                    }).create()
    else:
        latest_result_html = ''
    
    html_cal = cal.formatmonth(withyear=True)
    cal_container_title = Component('container',{"type":'h4',"class":'','content':"Upcomming Matches"}).create()
    cal_container = Component('container',{"type":'div',"class":'home_cal','content':html_cal}).create()
    
    calendar = Component('container',{"type":'div',"class":'home_calendar_with_title','content':cal_container_title+cal_container}).create()
    
    result_container_title = Component('container',{"type":'h4',"class":'','content':"Latest Result"}).create()
    result_container = Component('container',{"type":'div',"class":'latest_result_container','content':latest_result_html}).create()
    
    result = Component('container',{"type":'div',"class":'latest_result_with_title','content':result_container_title+result_container}).create()
    
    home_container = Component('container',{"type":'div',"class":'home_container','content':result+calendar}).create()
    return render(request, 'system/home.html', {'title': '', 'form':home_container})




def accountSummary(request):
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
