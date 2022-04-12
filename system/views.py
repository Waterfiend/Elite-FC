from calendar import calendar
import hashlib

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from .models import Permission, User,FieldReservation,AccountSummary,Discounts,Ticket,Match,Role,Tier,Salary
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
    conditions = Component('container',{'type':'p','class':'account-summary-text','content':
        '''Payments can be made at the Elite Club cashiers And at the Banks in cash or CERTIFIED checksBased 
        on the format: "Name of the bank, Elite Club Account"Payment for till February 28,2022 InclusiveList of accepted Banks 
        for Payments are :BANKMED, AUDI sal, BYBLOS, BML, SGBL, ARAB, BLOM, FransaFor Bank Transfers to CITIBANK, 
        Account: EliteFCIBAN LB94011500000000000600224166 for USDIBAN LB22011500000000000600224395 for INTERNATIONAL TRANSFERS ONLYIBAN LB69011500000000000600224034 for LBPSwift Code CITILBBEAUB VAT # 123329-601 / Club Fees are VAT 11% 
        exempt.Fees could be paid in US Dollars or Lebanese Poundsat the exchange rate prevailing at the time of payment'''}).create()
    print(conditions)
    return render(request,'system/form.html',{'title':title,'form':table+conditions}) 

def tierEnrollment(request):
    title= 'Tier Enrollment'
    user = User.objects.filter(email=request.session['login']['email']).first()
    if user.role in ['fan','admin']:
        tiers = Discounts.objects.all()
        tableOptions ={
                'table_header':['Tier', 'Discount Percentage','Fee ($/month)'],
                'table_rows':[
                ]     
            }
            
        for deatail in tiers:  
            selectLinkOptions ={
                'url':'/tierSelection/'+str(deatail.id),
                'text':'Select',
                'class':'btn btn-dark'
            }
            selectLink = Component('link',selectLinkOptions).create()
            fee = -Salary.objects.filter(role='fan',fan_tier=deatail.fan_tier).first().salary
            tableOptions['table_rows'].append([deatail.fan_tier,str(deatail.discount),str(fee),selectLink])
        table = Component('table',tableOptions).create()
    else:
        table = Component('container',{'type':'h3','content':'Sorry, You must be a fan to use this feature'}).create()
    return render(request,'system/form.html',{'title':title,'form':table}) 

def tierSelection(request,id):
    user = User.objects.filter(email=request.session['login']['email']).first()
    user.fan_tier= Discounts.objects.filter(id=id).first().fan_tier
    user.save()
    messages.success(request,'Tier changed successfully')
    return redirect('/tierEnrollment')

