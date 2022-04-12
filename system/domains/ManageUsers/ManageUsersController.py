from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from ...models import User,Role,Tier
from django.contrib import messages

from helpers.SearchBar import Search
import hashlib


def manageUsers(request):
    # searchBarOptions = {'submit_class':'','input_classes':{'0':''},'form_class':'','method':'POST','action':'/manageUser/',
    #         'form_fields':[
    #             {'label':'','input_props':{'name':'search','type':'text','placeholder':'Search Bar'}},
    # ]}
    # searchBar = Component('form',searchBarOptions).create(request).replace('required','',1)
    
    # if request.method=='POST':
    #     search = request.POST['search']
    #     filterCondition = Q(('full_name__icontains',search))|Q(email__icontains=search)|Q(role__icontains=search)|Q(fan_tier__icontains=search)
    #     users = User.objects.annotate(full_name=Concat('first_name',Value(' '),'last_name',output_field=CharField())).filter(filterCondition).all()
    # else:
    concatination = {'full_name':['first_name',' ','last_name']}
    (searchBar,users) = Search(request,User,concatination)
    users = users or User.objects.all()
    tableOptions ={
            'table_header':['Name', 'Email', 'Role','Tier' 'Edit', 'Delete'],
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
        tableOptions['table_rows'].append([user.first_name+" "+user.last_name,user.email,user.role,user.fan_tier,editLink,deleteLink])
    form = Component('table',tableOptions).create()    
    
    addLinkOptions ={
            'url':'/editUserPage/'+str(0),
            'text':'Add User',
            'class':'btn btn-success'
        }
    addLink = Component('link',addLinkOptions).create()
    backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
        }
    backLink = Component('link',backLinkOptions).create() 
      
    return render(request,'system/form.html',{'title':'Manage Users','form':backLink+addLink+searchBar+form})

def manageUserForm(request,id=0):
    if id != 0:
        existingUser = User.objects.filter(id=id).first()
        title = 'Edit ' + existingUser.first_name
        values = existingUser.__dict__
    else:
        title = 'Add User'
        values = {field.name:'' for field in User._meta.fields}
    tiers = []
    for tier in Tier.objects.all():
        tiers.append(tier.fan_tier)
    roles = []
    for role in Role.objects.all():
        roles.append(role.role)
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
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['First Name_input','Last Name_input','Email_input','Password_input','Confirm Password_input', 'Birth Date_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    backLinkOptions ={
            'url':'/manageUser/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
        }
    backLink = Component('link',backLinkOptions).create() 
    # confirmPasswordValidationScript = ConfirmPasswordErrorJS('Password_input','Confirm Password_input')
    # confirmPasswordValidationScriptComponenet = Component('script',confirmPasswordValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})
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
    
def deleteUser(request,id):
    existingRecord = User.objects.filter(id=id)
    existingRecord.delete()
    return redirect('/manageUser')
    
