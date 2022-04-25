from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from ...models import Permission, User,Tier
from django.contrib import messages
import hashlib


'''
renderRegistration is a function that is used to render the registration form that is filled by a user to create an account
'''
def renderRegistration(request):

    title = 'Registration Form'
    
    tiers = []
    for tier in Tier.objects.all():
        tiers.append(tier.fan_tier)
    
    # Define a registration form with its method and action and styling css class
    # Define the fields that the user will need to enter to make a proper registration request
    formOptions = {'form_class':'form','method':'POST','action':'/registerValidate/',
        'form_fields':[
            {'label':'First Name','input_props':{'name':'first_name','type':'text', 'pattern':"[A-Za-z\s]+", 'title':'Only letters allowed'}},
            {'label':'Last Name','input_props':{'name':'last_name','type':'text', 'pattern':"[A-Za-z\s]+", 'title':'Only letters allowed'}},
            {'label':'Email','input_props':{'name':'email','type':'email', 'pattern':'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}','placeholder':'email@email.com', 'title':'This is not an email'}},
            {'label':'Password','input_props':{'name':'password','type':'password'}},
            {'label':'Confirm Password','input_props':{'name':'confirm_password','type':'password'}},
            {'label':'Birth Date','input_props':{'name':'date_of_birth','type':'date'}},
            {'label':'Fan Tier','field_type':'select','input_props':{'name':'fan_tier','type':'text'},'select_options':tiers},
        ]}
    form = Component('form',formOptions).create(request) #create the form

    # this JavaScript is used render the validation errors that result when the user fills a field with incorrectly formatted data
    formValidationScript = FormValidationErrorsJS(['First Name_input','Last Name_input','Email_input','Password_input','Confirm Password_input', 'Birth Date_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create() # create the script componenet
    
    # JavaScript used to validate that user entered a confirmed password that is identical to the password
    confirmPasswordValidationScript = ConfirmPasswordErrorJS('Password_input','Confirm Password_input')
    confirmPasswordValidationScriptComponenet = Component('script',confirmPasswordValidationScript).create() # create the script componenet
    
    # inject the form, formValidationScriptComponenet, confirmPasswordValidationScriptComponenet into the form.html to render the page with the needed javascripts
    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet+confirmPasswordValidationScriptComponenet})

'''
validateRegistration is a function used to validated the information filled in the registration form.
If an email provided is already in use, an error is issued and the user is asked to repeat the registration.
'''
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

'''
renderLogin is a function used to render the login form used by users to access their accounts.
'''
def renderLogin(request):
    title = 'Login Form'
    
    # Define a login form with its method and action and styling css class
    # Define the fields that the user will need to enter to make a proper login request
    formOptions = {'form_class':'form','method':'GET','action':'/loginValidate/',
        'form_fields':[
            {'label':'Email','input_props':{'name':'email','type':'email','pattern':'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}', 'placeholder':'email@email.com', 'title':'This is not an email'}},
            {'label':'Password','input_props':{'name':'password','type':'password'}},
        ]}
    form = Component('form',formOptions).create(request)

    # this JavaScript is used render the validation errors that result when the user fills a field with incorrectly formatted data
    formValidationScript = FormValidationErrorsJS(['Email_input','Password_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create() #create script
    
    # inject the form, formValidationScriptComponenet, confirmPasswordValidationScriptComponenet into the form.html to render the page with the needed javascripts
    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet})


'''
validateLogin is a function used to validate that a proper login has taken place.
The email and hashed password provided by the user shoud match the email and password stored in the database for this user
'''
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

'''
profileLinks is a function used to generate the links accessable to the user on his profile page.
Some links are sensitive and are only generated with users who have the permission
'''
def profileLinks(request):
    user = User.objects.filter(email=request.session['login']['email']).first()
    
    # a dictionary of paths that are considered sensitive and should only be accessed for those with permission
    sensitivePaths = {'Manage Users':'/manageUser','Manage Schedule':'/schedule','Manage Tickets':'/Tickets','Manage Articles':'/News','Manage Player Info':'/PlayerStat','Manage Player Matches':'/Players','Manage Teams':'/Teams','Manage Salaries/Fees':'/manageFeesSalaries','Manage Permissions':'/managePermissions','Match Report':'/selectMatch','Financial Report':'/selectDate'}
    generatedSensitiveLinks=[]
    # go over the sensitive paths and create a link componenet only if the user has permission
    for key,value in sensitivePaths.items():
        AllowedRoles = Permission.objects.filter(path=value).values_list('role',flat=True)
        if user.role in AllowedRoles:
            link = Component('link',{'url':value+'/', 'text':key}).create()
        else:
            link = ''
        generatedSensitiveLinks.append(link)
        
    accountSummaryLink = Component('link',{'url':'/accountSummary/', 'text':'Account Summary'}).create() # create link to  user's account summary page
    myTicketsLink = Component('link',{'url':'/myTickets/', 'text':'My Tickets'}).create()# create link to user's tickets page
    myReservationsLink =Component('link',{'url':'/myReservations/', 'text':'My Reservations'}).create()# create link to user's reservations page
    changePasswordLink = Component('link',{'url':'/changePasswordandEmailForm/', 'text':'Change Credentials'}).create()# create link to user's change password page
    
    # use the sensitive links to create a division (container) componenet for the staff controls
    staffControlsDivisionTitle = Component('container',{'type':'h4', 'content':'Staff Control'}).create()
    staffControlsDivision = Component('container',{'type':'div', 'class':'linkContainer','content':staffControlsDivisionTitle+"".join(generatedSensitiveLinks)}).create()
    
    # create a division (container) for the account summary, ticketsm reservations, and change password links
    servicesDivisionTitle = Component('container',{'type':'h4', 'content':'Services'}).create()
    servicesDivision = Component('container',{'type':'div','class':'linkContainer', 'content':servicesDivisionTitle+accountSummaryLink+myTicketsLink+myReservationsLink+changePasswordLink}).create()

    menuTitle = Component('container',{'type':'summary', 'content':'Open Menu', 'class':'open-menu'}).create()
    menuContianer = Component('container',{'type':'div', 'class':'profileLinksMenu','content':servicesDivision+staffControlsDivision}).create()
    profileLinksMenu = Component('container',{'type':'details', 'content':menuTitle+menuContianer}).create()
    return profileLinksMenu

'''
renderProfile renders the profile page of the logged in user
This includes the user's personal information and the links generated using the profileLinks function
'''
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
'''
changePasswordandEmailForm is a function used to update the password and email of the user. The user is logged out if the operation is successful
The operation fails if the user chooses an email that is already taken
'''
def changePasswordandEmailForm(request):
    title = 'Change Email and Password'
    
    # Define the form and the fields required from the user to fill to change his email and password
    formOptions = {'form_class':'form','method':'POST','action':'/validatePassword/',
        'form_fields':[
            {'label':'Email','input_props':{'name':'email','type':'email', 'pattern':'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}','placeholder':'email@email.com', 'title':'This is not an email','value':request.session['login']['email']}},
            {'label':'New Password','input_props':{'name':'password','type':'password'}},
            {'label':'Confirm Password','input_props':{'name':'confirm_password','type':'password'}},
        ]}
    form = Component('form',formOptions).create(request) #create the form from formOptions

    # this JavaScript is used render the validation errors that result when the user fills a field with incorrectly formatted data
    formValidationScript = FormValidationErrorsJS(['Email_input','New Password_input','Confirm Password_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    # JavaScript used to validate that user entered a confirmed password that is identical to the password
    confirmPasswordValidationScript = ConfirmPasswordErrorJS('New Password_input','Confirm Password_input')
    confirmPasswordValidationScriptComponenet = Component('script',confirmPasswordValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet+confirmPasswordValidationScriptComponenet})

'''
validatePassword function is used to validate the email and passwords choosen by the user.
It fails if the email already exists
'''
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

'''
logout logs out the user from his session
'''
def logout(request):
    if 'login' in request.session:
        request.session.pop('login')
    return redirect('/')