from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from ...models import User
from django.contrib import messages
import hashlib


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
            # {'label':'Password','input_props':{'name':'password','type':'password'}},
            # {'label':'Confirm Password','input_props':{'name':'confirm_password','type':'password'}},
            {'label':'Birth Date','input_props':{'name':'date_of_birth','type':'date','value':values['date_of_birth']}},
            {'label':'Fan Tier','field_type':'select','input_props':{'name':'fan_tier','type':'text','value':values['fan_tier']},'select_options':['Bronze','Silver','Gold','Elite']},
            {'label':'Role','field_type':'select','input_props':{'name':'role','type':'text','value':values['role']},'select_options':['fan','coach','player','journalist','admin']},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['First Name_input','Last Name_input','Email_input','Password_input','Confirm Password_input', 'Birth Date_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    # confirmPasswordValidationScript = ConfirmPasswordErrorJS('Password_input','Confirm Password_input')
    # confirmPasswordValidationScriptComponenet = Component('script',confirmPasswordValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':form+formValidationScriptComponenet})
def editUserValidate(request,id):
    if(request.method == 'POST'):
        infoDict = {}
        for key in request.POST:
            infoDict[key]=request.POST[key]
        infoDict.pop('csrfmiddlewaretoken')
        # infoDict.pop('confirm_password')
        
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
                infoDict['password'] = hashlib.md5(infoDict['date_of_birth'].encode('utf-8')).hexdigest()
                User.objects.create(**infoDict)
                messages.success(request,'Add Successful')
        return redirect('/manageUser')
    
def deleteUser(request,id):
    existingRecord = User.objects.filter(id=id)
    existingRecord.delete()
    return redirect('/manageUser')
    
