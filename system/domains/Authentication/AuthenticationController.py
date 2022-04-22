from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from ...models import Permission, User,Tier
from django.contrib import messages
import hashlib

def renderRegistration(request):

    title = 'Registration Form'
    
    tiers = []
    for tier in Tier.objects.all():
        tiers.append(tier.fan_tier)
    
    formOptions = {'form_class':'form','method':'POST','action':'/registerValidate/',
        'form_fields':[
            {'label':'First Name','input_props':{'name':'first_name','type':'text', 'pattern':"[A-Za-z\s]+", 'title':'Only letters allowed'}},
            {'label':'Last Name','input_props':{'name':'last_name','type':'text', 'pattern':"[A-Za-z\s]+", 'title':'Only letters allowed'}},
            {'label':'Email','input_props':{'name':'email','type':'email', 'placeholder':'email@email.com', 'title':'This is not an email'}},
            {'label':'Password','input_props':{'name':'password','type':'password'}},
            {'label':'Confirm Password','input_props':{'name':'confirm_password','type':'password'}},
            {'label':'Birth Date','input_props':{'name':'date_of_birth','type':'date'}},
            {'label':'Fan Tier','field_type':'select','input_props':{'name':'fan_tier','type':'text'},'select_options':tiers},
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
            {'label':'Email','input_props':{'name':'email','type':'email', 'placeholder':'email@email.com', 'title':'This is not an email'}},
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
    sensitivePaths = {'Manage Users':'/manageUser','Manage Schedule':'/schedule','Manage Tickets':'/Tickets','Manage Articles':'/News','Manage Player Info':'/PlayerStat','Manage Player Matches':'/Players','Manage Teams':'/Teams','Manage Salaries/Fees':'/manageFeesSalaries','Manage Permissions':'/managePermissions','Match Report':'/selectMatch','Financial Report':'/selectDate'}
    generatedSensitiveLinks=[]
    for key,value in sensitivePaths.items():
        AllowedRoles = Permission.objects.filter(path=value).values_list('role',flat=True)
        if existingRecord.role in AllowedRoles:
            link = Component('link',{'url':value+'/', 'text':key}).create()
        else:
            link = ''
        generatedSensitiveLinks.append(link)
        
    accountSummaryLink = Component('link',{'url':'/accountSummary/', 'text':'Account Summary'}).create()
    reportsLink = Component('link',{'url':'/myTickets/', 'text':'My Tickets'}).create()
    changePasswordLink = Component('link',{'url':'/changePasswordandEmailForm/', 'text':'Change Credentials'}).create()
    
    staffControlsDivisionTitle = Component('container',{'type':'h4', 'content':'Staff Control'}).create()
    staffControlsDivision = Component('container',{'type':'div', 'class':'linkContainer','content':staffControlsDivisionTitle+"".join(generatedSensitiveLinks)}).create()
    
    servicesDivisionTitle = Component('container',{'type':'h4', 'content':'Services'}).create()
    servicesDivision = Component('container',{'type':'div','class':'linkContainer', 'content':servicesDivisionTitle+accountSummaryLink+reportsLink+changePasswordLink}).create()

    menuTitle = Component('container',{'type':'summary', 'content':'Open Menu'}).create()
    menuContianer = Component('container',{'type':'div', 'class':'profileLinksMenu','content':servicesDivision+staffControlsDivision}).create()
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
def changePasswordandEmailForm(request):
    title = 'Change Email and Password'
    
    formOptions = {'form_class':'form','method':'POST','action':'/validatePassword/',
        'form_fields':[
            {'label':'Email','input_props':{'name':'email','type':'email', 'placeholder':'email@email.com', 'title':'This is not an email','value':request.session['login']['email']}},
            {'label':'New Password','input_props':{'name':'password','type':'password'}},
            {'label':'Confirm Password','input_props':{'name':'confirm_password','type':'password'}},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['New Password_input','Confirm Password_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    confirmPasswordValidationScript = ConfirmPasswordErrorJS('New Password_input','Confirm Password_input')
    confirmPasswordValidationScriptComponenet = Component('script',confirmPasswordValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet+confirmPasswordValidationScriptComponenet})
def validatePassword(request):
    infoDict = {}
    for key in request.POST:
        infoDict[key]=request.POST[key]
    infoDict.pop('csrfmiddlewaretoken')
    infoDict.pop('confirm_password')
    infoDict['password'] = hashlib.md5(infoDict['password'].encode('utf-8')).hexdigest()
    try:
            existingEmailRecord = User.objects.filter(email=infoDict['email']).first()
    except:
        existingEmailRecord = None
    
    if(existingEmailRecord is not None and existingEmailRecord.id != id):
        messages.error(request,'Email '+ infoDict['email'] +' already exists. Please use a different email')
        return redirect('/Profile')
    else:
        try:
            existingRecord = User.objects.filter(email=request.session['login']['email']).first()
        except:
            existingRecord = None
        existingRecord.__dict__.update(infoDict)
        existingRecord.save()
        messages.success(request,'Update Successful')
        return redirect('/logout')
def logout(request):
    if 'login' in request.session:
        request.session.pop('login')
    return redirect('/')