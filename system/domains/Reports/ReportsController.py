from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS
from ...models import User,Ticket,Match,AccountSummary,Discounts
from django.contrib import messages
from django.db.models import Sum
from helpers.SearchBar import Search
import re


def selectMatch(request):
    
    title = 'Select Match'
    matches = Match.objects.all()
    match_ids = []
    backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
    backLink = Component('link',backLinkOptions).create()
    for match in matches:
        match_ids.append("<!--"+str(match.id)+"-->"+match.date+" "+match.time+" "+match.team1+"VS"+match.team2)

    formOptions = {'form_class':'form','method':'POST','action':'/selectMatch/',
        'form_fields':[
            {'label':'Match','field_type':'select','input_props':{'name':'match','type':'text','size':'4'},'select_options': match_ids},

        ]}
    form = Component('form',formOptions).create(request)
    if (request.method == 'POST'):
        infoDict = request.POST.copy() # POST takes all what is in Form from submit
        matchInfo = infoDict['match']
        id = re.search(r'<!--(.*?)-->', matchInfo).group(1)
        return redirect('/renderMatch/'+str(id))
    formValidationScript = FormValidationErrorsJS(['Match_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()


    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})

def renderMatch(request,id):
    match = Match.objects.filter(id=id).first()
    try:
        existingRecord = Ticket.objects.filter(match=match).first() # match of model = match fetched
    except:
        existingRecord = None
    if(existingRecord is None):
        messages.error(request,'Tickets Were Not Set For Match')
        return redirect('/Profile/')
    else:
        tableOptions ={
            'table_header':['Fan Name', "Ticket Type", "Price"],
            'table_rows':[],     
        }
        generalAdmission = AccountSummary.objects.filter(transaction_name__contains="Ticket").filter(transaction_name__contains="General Admission")
        vip = AccountSummary.objects.filter(transaction_name__contains="Ticket").filter(transaction_name__contains="VIP")
        reserved = AccountSummary.objects.filter(transaction_name__contains="Ticket").filter(transaction_name__contains="Reserved")
        
        # for record in generalAdmission:
        #     tableOptions['table_rows'].append([str(record.user), "General Admission", str(record.transaction_amount)])
        # for record in vip:
        #     tableOptions['table_rows'].append([str(record.user), "VIP", str(record.transaction_amount)])
        # for record in reserved:
        #     tableOptions['table_rows'].append([str(record.user), "Reserved", str(record.transaction_amount)])
        records = generalAdmission|vip|reserved
        concatination = {'full_name':['user__first_name',' ','user__last_name']}
        (searchBar,fiteredRecords) = Search(request,records,concatination)
        print(fiteredRecords)
        records = fiteredRecords or records
        for record in records:
            pat = re.compile('(General Admission|VIP|Reserved)')
            ticketType = pat.search(record.transaction_name).group(1)
            tableOptions['table_rows'].append([str(record.user), ticketType, str(record.transaction_amount)])
        Total = records.aggregate(Sum('transaction_amount'))
        tableOptions['table_rows'].append(['', "Total", str(Total['transaction_amount__sum'])])
        form = Component('table',tableOptions).create()
        return render(request,'system/form.html', {'title':'Available Tickets','form':searchBar+form })
def selectDate(request):
    title = 'Select Month'
    backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
            }
    backLink = Component('link',backLinkOptions).create()

    formOptions = {'form_class':'form','method':'POST','action':'/financialSummary/',
        'form_fields':[
            {'label':'Month','input_props':{'name':'month','type':'month'}},

        ]}
    form = Component('form',formOptions).create(request)
    formValidationScript = FormValidationErrorsJS(['Month_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})
def financialSummary(request):
    if request.method == 'POST':
        month = request.POST['month']
        monthRecords = AccountSummary.objects.filter(date__contains=month)
        salariesSum = monthRecords.filter(transaction_name__contains='Salary').aggregate(Sum('transaction_amount'))
        feesSum = monthRecords.filter(transaction_name__contains='Fee').aggregate(Sum('transaction_amount'))
        ticketSum = monthRecords.filter(transaction_name__contains='Ticket').aggregate(Sum('transaction_amount'))
        reservationSum = monthRecords.filter(transaction_name__contains='Reservation').aggregate(Sum('transaction_amount'))
        totalSum = monthRecords.aggregate(Sum('transaction_amount'))
        tableOptions ={
            'table_header':['Name', "Total"],
            'table_rows':[],     
        }
        tableOptions['table_rows'].append(["Salaries", str(salariesSum['transaction_amount__sum'])])
        tableOptions['table_rows'].append(["Fees", str(feesSum['transaction_amount__sum'])])
        tableOptions['table_rows'].append(["Tickets", str(ticketSum['transaction_amount__sum'])])
        tableOptions['table_rows'].append(["Reservations", str(reservationSum['transaction_amount__sum'])])
        tableOptions['table_rows'].append(["Total", str(totalSum['transaction_amount__sum'])])
        form = Component('table',tableOptions).create()
        return render(request,'system/form.html',{'title':'Financial Summary','form':form})