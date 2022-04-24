from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS
from ...models import Salary,Tier,Role,AccountSummary,User
from django.contrib import messages
from helpers.SearchBar import Search
import datetime
from django.db.models import Q

'''
manageFeesSalaries function renders the fees and salaries page. 
It shows a table with the fee/salary for various role-tier combinations
it shows a delete button for each fee/salary
There is an add button used to add new fee/salary combinations
There is a submit fees/salaries button that submits the fees to the users' account summaries
There is a rollback button that allows undoing submissions while within the same month
There is a search bar that allows you to filter based on user input
'''
def manageFeesSalaries(request):
    # define the button that takes us to the create fee/salary form where we define fees for role-tier combinations
    addOptions = {
                'url':'/CreateFeesSalaries/',
                'text':'Add Salary/Fee',
                'class':'btn btn-success me-1'
            }
    addLink = Component('link', addOptions).create()
    
    # create the cubmit button that adds the fee/salary to the user account summaries
    submitOptions = {
                'url':'/feesSalariesSubmit/',
                'text':'Submit Salaries/Fees',
                'class':'btn btn-danger me-1'
            }
    submitLink = Component('link', submitOptions).create()
    
    #add the button that allows for rolling back submitted fees/salaries within the same month
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
    # table options used in creating the fee/salary table
    tableOptions ={
                'table_header':['Role','Trier', 'Salary/Fee',],
                'table_rows':[],     
            }
    
    # use the Search function to create a new instance of the search filter and return a filtered set of users based on the user input in the search bar
    concatination = {}
    (searchBar,users) = Search(request,Salary,concatination)
    salaryCategories = users or Salary.objects.all()
    # for each salary type display the role, tier, and amount
    for category in salaryCategories:
        deleteLinkOptions ={# define the delete button for each salary category
        'url':'/deleteFeesSalaries/'+str(category.id),
        'text':'Delete',
        'class':'btn btn-danger'
        }
        deleteLink = Component('link', deleteLinkOptions).create()#create the delete button componenet
        tableOptions['table_rows'].append([category.role, category.fan_tier,str(category.salary), deleteLink])# add salary info into the table for the given salary category

    form = Component('table',tableOptions).create()
    return render(request,'system/form.html', {'title':'Salaries/Fees','form':backLink+addLink+submitLink+rollbackLink+searchBar+form })

'''
deleteFeesSalaries function deletes a fee/salary by id
'''
def deleteFeesSalaries(request,id):
    existingRecord = Salary.objects.filter(id=id)
    existingRecord.delete()
    return redirect('/manageFeesSalaries/')

'''
CreateFeesSalaries function renders the form used to create a new fee/salary category
'''
def CreateFeesSalaries(request):
    
    #get all tiers
    tiers = []
    for tier in Tier.objects.all():
        tiers.append(tier.fan_tier)
    #get all roles
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
    
    # define the form and the form fields required by the user to create a fee category
    formOptions = {'form_class':'form','method':'POST','action':'/feesSalariesValidate/',
        'form_fields':[
            {'label':'Fan Tier','field_type':'select','input_props':{'name':'fan_tier','type':'text'},'select_options':tiers},
            {'label':'Role','field_type':'select','input_props':{'name':'role','type':'text'},'select_options':roles},
            {'label':'Salary/Fee','input_props':{'name':'salary','type':'number'}},
        ]}
    form = Component('form',formOptions).create(request)# create form

    # this JavaScript is used render the validation errors that result when the user fills a field with incorrectly formatted data   
    formValidationScript = FormValidationErrorsJS(['Role_input','Fan Tier_input','Salary/Fee_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    #inject form and scripts into the form.html
    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})
'''
feesSalariesValidate function validates the created fee/summary category
Returns an error if the fee/salary category already exists
'''
def feesSalariesValidate(request, id = 0):
    if(request.method == 'POST'):
        infoDict = request.POST.copy() # POST takes all what is in Form from submit
        try:
            salaryType = Salary.objects.filter(role=infoDict["role"],fan_tier=infoDict["fan_tier"])
        except:
            salaryType = None
        if salaryType is None:
            Salary.objects.create(role=infoDict["role"], fan_tier=infoDict["fan_tier"],salary=infoDict["salary"])
            messages.success(request,'Salary/Fee Category Successfully Added')
        else:
            messages.success(request,'Salary/Fee Category Exists')
        return redirect('/manageFeesSalaries/')

'''
feesSalariesSubmit function submits the fee/salary to the account summary of each user for each fee/salary category
'''
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
'''
feesSalariesRollback function undos the last fee submission within the same month
'''
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