from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS
from ...models import Salary,Tier,Role,AccountSummary,User
from django.contrib import messages
from helpers.SearchBar import Search
import datetime
from django.db.models import Q
def manageFeesSalaries(request):
    addOptions = {
                'url':'/CreateFeesSalaries/',
                'text':'Add Salary/Fee',
                'class':'btn btn-success me-1'
            }
    addLink = Component('link', addOptions).create()
    submitOptions = {
                'url':'/feesSalariesSubmit/',
                'text':'Submit Salaries/Fees',
                'class':'btn btn-danger me-1'
            }
    submitLink = Component('link', submitOptions).create()
    rollbackOptions = {
                'url':'/feesSalariesRollback/',
                'text':'Rollback Salaries/Fees',
                'class':'btn btn-danger me-1'
            }
    rollbackLink = Component('link', rollbackOptions).create()
    
    backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
    }
    backLink = Component('link',backLinkOptions).create()
    tableOptions ={
                'table_header':['Role','Trier', 'Salary/Fee',],
                'table_rows':[],     
            }
    concatination = {}
    (searchBar,users) = Search(request,Salary,concatination)
    salaries = users or Salary.objects.all()
    for salary in salaries:
        deleteLinkOptions ={
        'url':'/deleteFeesSalaries/'+str(salary.id),
        'text':'Delete',
        'class':'btn btn-danger'
        }
        deleteLink = Component('link', deleteLinkOptions).create()
        tableOptions['table_rows'].append([salary.role, salary.fan_tier,str(salary.salary), deleteLink])

    form = Component('table',tableOptions).create()
    return render(request,'system/form.html', {'title':'Salaries/Fees','form':backLink+addLink+submitLink+rollbackLink+searchBar+form })
def deleteFeesSalaries(request,id):
    existingRecord = Salary.objects.filter(id=id)
    existingRecord.delete()
    return redirect('/manageFeesSalaries/')

def CreateFeesSalaries(request):
    
    tiers = []
    for tier in Tier.objects.all():
        tiers.append(tier.fan_tier)
    roles = []
    for role in Role.objects.all():
        roles.append(role.role)
    title = 'Create Permission'
    backLinkOptions ={
            'url':'/manageFeesSalaries/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
    }
    backLink = Component('link',backLinkOptions).create()
    formOptions = {'form_class':'form','method':'POST','action':'/feesSalariesValidate/',
        'form_fields':[
            {'label':'Fan Tier','field_type':'select','input_props':{'name':'fan_tier','type':'text'},'select_options':tiers},
            {'label':'Role','field_type':'select','input_props':{'name':'role','type':'text'},'select_options':roles},
            {'label':'Salary/Fee','input_props':{'name':'salary','type':'number'}},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['Role_input','Fan Tier_input','Salary/Fee_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})
def feesSalariesValidate(request, id = 0):
    if(request.method == 'POST'):
        infoDict = request.POST.copy() # POST takes all what is in Form from submit
        Salary.objects.create(role=infoDict["role"], fan_tier=infoDict["fan_tier"],salary=infoDict["salary"])
        messages.success(request,'Salary/Fee Successfully Added')

        return redirect('/manageFeesSalaries/')
def feesSalariesSubmit(request):
    salariesTypes = Salary.objects.all()
    for type in salariesTypes:
        tier = type.fan_tier
        role = type.role
        amount = - type.salary
        try:
            users = User.objects.filter(role=role,fan_tier=tier)
        except:
            users = []
        dt = datetime.datetime.today()
        today = dt.strftime('%Y-%m-%d')
        for user in users:
            if amount>0:
                AccountSummary.objects.create(user=user,transaction_name="Fee "+str(dt.year)+'-'+str(dt.month),transaction_amount=amount,date=today)
            elif amount<0:
                AccountSummary.objects.create(user=user,transaction_name="Salary "+str(dt.year)+'-'+str(dt.month),transaction_amount=amount,date=today)
    messages.success(request,'Salary/Fee Successfully Submitted')
    return redirect('/manageFeesSalaries/')

def feesSalariesRollback(request):
    dt = datetime.datetime.today()
    filterCondition = Q(transaction_name="Fee "+str(dt.year)+'-'+str(dt.month))|Q(transaction_name="Salary "+str(dt.year)+'-'+str(dt.month))
    accountsSalaries = AccountSummary.objects.filter(filterCondition)
    if accountsSalaries:
        accountsSalaries.delete()
        messages.success(request,'Salary/Fee Successfully Removed')
    else:
        messages.error(request,'Salary/Fee Does Not Exist')
    return redirect('/manageFeesSalaries/')