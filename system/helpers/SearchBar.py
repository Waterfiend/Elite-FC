from system.helpers.Component import Component
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.db.models import Q

def Search(request,model,concatinations):
    searchBarOptions = {'submit_class':'','input_classes':{'0':''},'form_class':'','method':'POST','action':request.path,
            'form_fields':[
                {'label':'','input_props':{'name':'search','type':'text','placeholder':'Filter'}},
    ]}
    searchBar = Component('form',searchBarOptions).create(request).replace('required','',1)
    try:
        items = model.objects
    except:
        items = model
    if request.method=='POST':
        search = request.POST['search']
        
        for concatination,values in concatinations.items():
            parameter = {concatination:Concat(values[0],Value(values[1]),values[2],output_field=CharField())}
            items =items.annotate(**parameter)
        
        filterCondition = Q()
        for concatination,values in concatinations.items(): 
            filterCondition = filterCondition|Q((concatination+'__icontains',search))
        try:
            columnNames = [field.name for field in model.model._meta.fields if field.get_internal_type() != 'ForeignKey']
        except:
            columnNames = [field.name for field in model._meta.fields if field.get_internal_type() != 'ForeignKey']
            
        for name in columnNames:
            filterCondition = filterCondition|Q((name+'__icontains',search))
        items = items.filter(filterCondition).all()
        print(items)
        return searchBar,items
    else:
        return searchBar,items.none()