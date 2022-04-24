from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from ...models import User,Role,Tier
from django.contrib import messages

from helpers.SearchBar import Search
import hashlib

'''
manageUsers function renders the manage users page. 
It shows a table with all users and their information
it shows a delete button for each user
it shows an edit button for each user
There is an add button used to add new user
There is a search bar that allows you to filter based on user input
'''
def manageUsers(request):
    # use the Search function to create a new instance of the search filter and return a filtered set of users based on the user input in the search bar
    concatination = {'full_name':['first_name',' ','last_name']} #Define a concatination: create full name from first and last name
    (searchBar,users) = Search(request,User,concatination)
    users = users or User.objects.all()
    
    #define the table options used in creating the users table.
    tableOptions ={
            'table_header':['Name', 'Email', 'Role','Tier' 'Edit', 'Delete'],
            'table_rows':[
            ]     
        }
    for user in users: # for each user in the users table, add its info in the table
        deleteLinkOptions ={# define a delete button for the user
            'url':'/deleteUser/'+str(user.id),
            'text':'Delete',
            'class':'btn btn-danger'
        }
        deleteLink = Component('link',deleteLinkOptions).create()# create the delete button for the user
        editLinkOptions ={#define an edit button for the user
            'url':'/editUserPage/'+str(user.id),
            'text':'Edit',
            'class':'btn btn-success'
        }
        editLink = Component('link',editLinkOptions).create() #create the edit button
        tableOptions['table_rows'].append([user.first_name+" "+user.last_name,user.email,user.role,user.fan_tier,editLink,deleteLink]) #insert user info as a table row
    table = Component('table',tableOptions).create()# create the users table    
    
    addLinkOptions ={# define a add user link
            'url':'/editUserPage/'+str(0),
            'text':'Add User',
            'class':'btn btn-success'
        }
    addLink = Component('link',addLinkOptions).create()# create the add user link
    backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
        }
    backLink = Component('link',backLinkOptions).create() 
    #inject buttons, user table, and the search bar into form.html
    return render(request,'system/form.html',{'title':'Manage Users','form':backLink+addLink+searchBar+table})
'''
manageUserForm function renders the form that should be filled to define a ne user or edit an existing user
'''
def manageUserForm(request,id=0): #id =0 is used to define new users mode
    if id != 0:# if id not 0, enter edit mode
        existingUser = User.objects.filter(id=id).first()
        title = 'Edit ' + existingUser.first_name
        values = existingUser.__dict__ # set values as the dictionary extracted from the filtered existing user
    else:# enter add new user mode
        title = 'Add User'
        values = {field.name:'' for field in User._meta.fields} # create a dictionary with empty values for each field in the user model
    # get all tiers
    tiers = []
    for tier in Tier.objects.all():
        tiers.append(tier.fan_tier)
    # get all roles
    roles = []
    for role in Role.objects.all():
        roles.append(role.role)
    
    # define the form that will be filled to create or edit a user
    formOptions = {'form_class':'form','method':'POST','action':'/editUserValidate/'+str(id),
        'form_fields':[
            {'label':'First Name','input_props':{'name':'first_name','type':'text', 'pattern':"[A-Za-z\s]+", 'title':'Only letters allowed', 'value':values['first_name']}},
            {'label':'Last Name','input_props':{'name':'last_name','type':'text', 'pattern':"[A-Za-z\s]+", 'title':'Only letters allowed','value':values['last_name']}},
            {'label':'Email','input_props':{'name':'email','type':'email', 'placeholder':'email@email.com', 'title':'Email must contain @','value':values['email']}},
            # {'label':'Password','input_props':{'name':'password','type':'password'}},
            # {'label':'Confirm Password','input_props':{'name':'confirm_password','type':'password'}},
            {'label':'Birth Date','input_props':{'name':'date_of_birth','type':'date','value':values['date_of_birth']}},
            {'label':'Fan Tier','field_type':'select','input_props':{'name':'fan_tier','type':'text','selected':values['fan_tier']},'select_options':tiers},
            {'label':'Role','field_type':'select','input_props':{'name':'role','type':'text','selected':values['role']},'select_options':roles},
        ]}
    form = Component('form',formOptions).create(request)# create the form component
    
    # this JavaScript is used render the validation errors that result when the user fills a field with incorrectly formatted data   
    formValidationScript = FormValidationErrorsJS(['First Name_input','Last Name_input','Email_input','Password_input','Confirm Password_input', 'Birth Date_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create() #create script component
    
    backLinkOptions ={# define back button
            'url':'/manageUser/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
        }
    backLink = Component('link',backLinkOptions).create() 
    # confirmPasswordValidationScript = ConfirmPasswordErrorJS('Password_input','Confirm Password_input')
    # confirmPasswordValidationScriptComponenet = Component('script',confirmPasswordValidationScript).create()
    
    # inject the buttons, form, and script into form.html
    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})
'''
editUserValidate function validates the user before saving them into the database. (id:user's id. 0 if a new user is created)
It validates that the created/edited user has a unique email. Otherwise it returns an error
If a new user is created, the default password is his birth date yyyy-mm-dd
'''
def editUserValidate(request,id):
    if(request.method == 'POST'):
        infoDict = {}
        for key in request.POST:
            infoDict[key]=request.POST[key]
        infoDict.pop('csrfmiddlewaretoken')
        # infoDict.pop('confirm_password')
        
        try:
            existingEmailRecord = User.objects.filter(email=infoDict['email']).first()
        except:
            existingEmailRecord = None
        
        if(existingEmailRecord is not None and existingEmailRecord.id != id):
            messages.error(request,'Email '+ infoDict['email'] +' already exists. Please use a different email')
        else:
            existingRecord = User.objects.filter(id=id).first()
            if id !=0:
                existingRecord.__dict__.update(infoDict)
                existingRecord.save()
                messages.success(request,'Update Successful')
            else:
                infoDict['password'] = hashlib.md5(infoDict['date_of_birth'].encode('utf-8')).hexdigest()
                User.objects.create(**infoDict)
                messages.success(request,'Add Successful')
        return redirect('/manageUser')
'''
deleteUser function deleted a user from the database based on their id
'''
def deleteUser(request,id):
    existingRecord = User.objects.filter(id=id)
    existingRecord.delete()
    return redirect('/manageUser')
    
