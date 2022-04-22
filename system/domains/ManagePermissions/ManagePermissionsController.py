from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS
from ...models import Permission
from django.contrib import messages
from helpers.SearchBar import Search

def managePermissions(request):
    addOptions = {
                'url':'/CreatePermission/',
                'text':'Add Permission',
                'class':'btn btn-success'
            }
    addLink = Component('link', addOptions).create()
    backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
    }
    backLink = Component('link',backLinkOptions).create()
    tableOptions ={
                'table_header':['Role', 'Allowed Paths',],
                'table_rows':[],     
            }
    concatination = {}
    (searchBar,users) = Search(request,Permission,concatination)
    permissions = users or Permission.objects.all()
    for permission in permissions:
        deleteLinkOptions ={
        'url':'/deletePermission/'+str(permission.id),
        'text':'Delete',
        'class':'btn btn-danger'
        }
        deleteLink = Component('link', deleteLinkOptions).create()
        tableOptions['table_rows'].append([permission.role, permission.path, deleteLink])

    form = Component('table',tableOptions).create()
    return render(request,'system/form.html', {'title':'Manage Permissions','form':backLink+addLink+searchBar+form })
def deletePermission(request,id):
    existingRecord = Permission.objects.filter(id=id)
    existingRecord.delete()
    return redirect('/managePermissions/')

def createPermission(request):
    title = 'Create Permission'
    backLinkOptions ={
            'url':'/managePermissions/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
    }
    backLink = Component('link',backLinkOptions).create()
    formOptions = {'form_class':'form','method':'POST','action':'/permissionValidate/',
        'form_fields':[
            {'label':'Role','input_props':{'name':'role','type':'text', 'pattern':"[A-Za-z1-9/_]+", 'title':'Only letters and numbers allowed'}},
            {'label':'Path','input_props':{'name':'path','type':'text', 'pattern':"[A-Za-z1-9/_]+", 'title':'Only letters and numbers allowed'}},
        ]}
    form = Component('form',formOptions).create(request)

    formValidationScript = FormValidationErrorsJS(['Role_input','Path_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})
def permissionValidate(request, id = 0):
    if(request.method == 'POST'):
        infoDict = request.POST.copy() # POST takes all what is in Form from submit
        Permission.objects.create(role=infoDict["role"], path=infoDict["path"])
        messages.success(request,'Permission Successfully Added')

        return redirect('/managePermissions/')
