from turtle import title
from django.shortcuts import render,redirect
from django.http import HttpResponse
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from .models import User
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
            request.session['login'] = infoDict.copy()
            messages.success(request,'Login Successful! Welcome '+ existingRecord.first_name)
        else:
            messages.error(request,'Login Failed: Wrong Credentials')

        return redirect('/Profile/')
def profileLinks(request):
    existingRecord = User.objects.filter(email=request.session['login']['email']).first()
    
    if existingRecord.role in ['admin']:
        manageUsersLink = Component('link',{'url':'/manageUser/', 'text':'Manage Users'}).create()
    else:
        manageUsersLink = ''
    if existingRecord.role in ['admin','staff']:
        manageScheduleLink = Component('link',{'url':'/manageUser/', 'text':'Manage Schedule'}).create()
    else:
        manageScheduleLink = ''
        
    if existingRecord.role in ['admin','staff']:
        manageTicketsLink = Component('link',{'url':'/manageUser/', 'text':'Manage Tickets'}).create()
    else:
        manageTicketsLink = ''
        
    if existingRecord.role in ['admin','journalist']:
        manageArticlesLink = Component('link',{'url':'/manageUser/', 'text':'Manage Articles'}).create()
    else:
        manageArticlesLink = ''
    
    if existingRecord.role in ['admin','couch']:
        managePlayersLink = Component('link',{'url':'/manageUser/', 'text':'Manage Players'}).create()
    else:
        managePlayersLink = ''
        
    accountSummaryLink = Component('link',{'url':'/manageUser/', 'text':'Account Summary'}).create()
    reportsLink = Component('link',{'url':'/manageUser/', 'text':'Reports'}).create()
    
    staffControlsDivisionTitle = Component('container',{'type':'h4', 'content':'Staff Control'}).create()
    staffControlsDivision = Component('container',{'type':'div', 'class':'linkContainer','content':staffControlsDivisionTitle+accountSummaryLink+reportsLink}).create()
    
    servicesDivisionTitle = Component('container',{'type':'h4', 'content':'Services'}).create()
    servicesDivision = Component('container',{'type':'div','class':'linkContainer', 'content':servicesDivisionTitle+manageUsersLink+manageScheduleLink+manageTicketsLink+manageArticlesLink+managePlayersLink}).create()

    menuTitle = Component('container',{'type':'summary', 'content':'Open Menu'}).create()
    menuContianer = Component('container',{'type':'div', 'class':'profileLinksMenu','content':staffControlsDivision+servicesDivision}).create()
    profileLinksMenu = Component('container',{'type':'details', 'content':menuTitle+menuContianer}).create()
    return profileLinksMenu

def renderProfile(request):
    if 'login' in request.session:
        existingRecord = User.objects.filter(email=request.session['login']['email']).first()
        title = 'Welcome '+existingRecord.first_name
        tableOptions ={
            'table_rows':[
            ]     
        }
        info = existingRecord.__dict__.copy()
        info.pop('_state')
        info.pop('password')
        for key,item in info.items():
            tableOptions['table_rows'].append([str(key),str(item)])
        form = Component('table',tableOptions).create()
        logoutLinkOptions ={
            'url':'/logout/',
            'text':'Logout',
            'class':'btn btn-dark'
        }
        logoutLink = Component('link',logoutLinkOptions).create()
        return render(request,'system/form.html',{'title':title,'form':profileLinks(request)+form+logoutLink})  
    else:
        return redirect('/')
def logout(request):
    if 'login' in request.session:
        request.session.pop('login')
    return redirect('/')

def manageUsers(request):
    users = User.objects.all()
    tableOptions ={
            'table_header':['Name', 'Email', 'Edit', 'Delete'],
            'table_rows':[
            ]     
        }
    for user in users:
        deleteLinkOptions ={
            'url':'/deleteUser/'+str(user.id),
            'text':'Delete',
            'class':'btn btn-danger'
        }
        deleteLink = Component('link',deleteLinkOptions).create()
        editLinkOptions ={
            'url':'/editUserPage/'+str(user.id),
            'text':'Edit',
            'class':'btn btn-success'
        }
        editLink = Component('link',editLinkOptions).create()   
        tableOptions['table_rows'].append([user.first_name+" "+user.last_name,user.email,editLink,deleteLink])
    form = Component('table',tableOptions).create()    
    
    addLinkOptions ={
            'url':'/editUserPage/'+str(0),
            'text':'Add User',
            'class':'btn btn-success'
        }
    addLink = Component('link',addLinkOptions).create()   
    return render(request,'system/form.html',{'title':'Manage Users','form':form+addLink})

def manageUserForm(request,id=0):
    if id != 0:
        existingUser = User.objects.filter(id=id).first()
        title = 'Edit ' + existingUser.first_name
        values = existingUser.__dict__
    else:
        title = 'Add User'
        values = {field.name:'' for field in User._meta.fields}
    
    formOptions = {'form_class':'form','method':'POST','action':'/editUserValidate/'+str(id),
        'form_fields':[
            {'label':'First Name','input_props':{'name':'first_name','type':'text', 'pattern':"[A-Za-z]+", 'title':'Only letters allowed', 'value':values['first_name']}},
            {'label':'Last Name','input_props':{'name':'last_name','type':'text', 'pattern':"[A-Za-z]+", 'title':'Only letters allowed','value':values['last_name']}},
            {'label':'Email','input_props':{'name':'email','type':'email', 'placeholder':'email@email.com', 'title':'Email must contain @','value':values['email']}},
            {'label':'Password','input_props':{'name':'password','type':'password'}},
            {'label':'Confirm Password','input_props':{'name':'confirm_password','type':'password'}},
            {'label':'Birth Date','input_props':{'name':'date_of_birth','type':'date','value':values['date_of_birth']}},
            {'label':'Fan Tier','field_type':'select','input_props':{'name':'fan_tier','type':'text','value':values['fan_tier']},'select_options':['Bronze','Silver','Gold','Elite']},
            {'label':'Role','field_type':'select','input_props':{'name':'role','type':'text','value':values['role']},'select_options':['fan','coach','player','journalist','admin']},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['First Name_input','Last Name_input','Email_input','Password_input','Confirm Password_input', 'Birth Date_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    confirmPasswordValidationScript = ConfirmPasswordErrorJS('Password_input','Confirm Password_input')
    confirmPasswordValidationScriptComponenet = Component('script',confirmPasswordValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet+confirmPasswordValidationScriptComponenet})
def editUserValidate(request,id):
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
        
        if(existingRecord is not None and existingRecord.id != id):
            messages.error(request,'Email '+ infoDict['email'] +' already exists. Please use a different email')
        else:
            if id !=0:
                existingRecord.__dict__.update(infoDict)
                existingRecord.save()
                messages.success(request,'Update Successful')
            else:
                User.objects.create(**infoDict)
                messages.success(request,'Add Successful')
        return redirect('/manageUser')
    
def deleteUser(request,id):
    existingRecord = User.objects.filter(id=id)
    existingRecord.delete()
    return redirect('/manageUser')
    
    