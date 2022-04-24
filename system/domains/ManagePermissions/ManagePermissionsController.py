from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS
from ...models import Permission
from django.contrib import messages
from helpers.SearchBar import Search
'''
managePermissions function renders the permissions page. 
It shows a table with the permissions for various roles
it shows a delete button for each permission
There is an add button used to add new permission
There is a search bar that allows you to filter based on user input
'''
def managePermissions(request):
    # Define the add buttom used to display the add permissions form
    addOptions = {
                'url':'/CreatePermission/',
                'text':'Add Permission',
                'class':'btn btn-success'
            }
    addLink = Component('link', addOptions).create()# create buttom
    backLinkOptions ={
            'url':'/Profile/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
    }
    backLink = Component('link',backLinkOptions).create()
    
    #define the table options used in creating the permissions table. (role column,allowed paths column)
    tableOptions ={
                'table_header':['Role', 'Allowed Paths',],
                'table_rows':[],     
            }
    
    # use the Search function to create a new instance of the search filter and return a filtered set of users based on the user input in the search bar
    concatination = {}
    (searchBar,users) = Search(request,Permission,concatination)
    permissions = users or Permission.objects.all()
    # form each permission display the role, path and, delete button
    for permission in permissions:
        deleteLinkOptions ={# define the delete button for each permission
        'url':'/deletePermission/'+str(permission.id),
        'text':'Delete',
        'class':'btn btn-danger'
        }
        deleteLink = Component('link', deleteLinkOptions).create()# create delete button
        tableOptions['table_rows'].append([permission.role, permission.path, deleteLink])# add permission infor into the table

    table = Component('table',tableOptions).create()# create permissions table table 
    return render(request,'system/form.html', {'title':'Manage Permissions','form':backLink+addLink+searchBar+table })

'''
deletePermission function deletes a permission based on the provided id
'''
def deletePermission(request,id):
    existingRecord = Permission.objects.filter(id=id)
    existingRecord.delete()
    return redirect('/managePermissions/')

'''
createPermission renders the create permission form used by the user to enter information of a new permission they want to create
'''
def createPermission(request):
    title = 'Create Permission'
    backLinkOptions ={
            'url':'/managePermissions/',
            'text':'Go Back',
            'class':'btn btn-dark me-1'
    }
    backLink = Component('link',backLinkOptions).create()
    
    formOptions = {'form_class':'form','method':'POST','action':'/permissionValidate/', # define the form and fields that allow users to enter information required to create permisions 
        'form_fields':[
            {'label':'Role','input_props':{'name':'role','type':'text', 'pattern':"[A-Za-z1-9/_]+", 'title':'Only letters and numbers allowed'}},
            {'label':'Path','input_props':{'name':'path','type':'text', 'pattern':"[A-Za-z1-9/_]+", 'title':'Only letters and numbers allowed'}},
        ]}
    form = Component('form',formOptions).create(request)# create the form

    # this JavaScript is used render the validation errors that result when the user fills a field with incorrectly formatted data   
    formValidationScript = FormValidationErrorsJS(['Role_input','Path_input'])
    formValidationScriptComponenet = Component('script',formValidationScript).create()
    
    return render(request,'system/form.html',{'title':title,'form':backLink+form+formValidationScriptComponenet})
'''
permissionValidate validates a permission before commiting it to the database
'''
def permissionValidate(request, id = 0):
    if(request.method == 'POST'):
        infoDict = request.POST.copy() # POST takes all what is in Form from submit
        Permission.objects.create(role=infoDict["role"], path=infoDict["path"])
        messages.success(request,'Permission Successfully Added')

        return redirect('/managePermissions/')
