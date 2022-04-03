from django.shortcuts import render,redirect
from system.helpers.Component import Component
from system.helpers.FormValidationJS import FormValidationErrorsJS
from ...models import User,FieldReservation,AccountSummary,Discounts
from django.contrib import messages
from datetime import datetime


def fieldReservation(request):
    if 'login' in request.session:
        title= 'Field Reservation'
        reservationCost = 15
        user = User.objects.filter(email=request.session['login']['email']).first()
        discount = Discounts.objects.filter(fan_tier=user.fan_tier).first()
        totalCharge = reservationCost*(100-discount.discount)/100
        discountMessage = Component('container',{'type':'h4','content':"Field reservation will cost you $"+str(totalCharge)+" after discount because you are "+ user.fan_tier+" tier"}).create()
        today = datetime.today().strftime('%Y-%m-%d')
        formOptions = {'form_class':'form','method':'POST','action':'/reservationValidate/',
            'form_fields':[
            
            
                {'label':'Reservation Date','input_props':{'name':'date','type':'date','min':today}},
                {'label':'Time','field_type':'select','input_props':{'name':'slot_time','type':'text'},'select_options':['9:00 AM-11:00 AM','9:00 AM-11:00 AM','11:00 AM-1:00 PM','1:00 PM-3:00 PM','3:00 PM-5:00 PM']},
            ]}
        form = Component('form',formOptions).create(request)
        tableOptions ={
                'table_header':['Reserved Date', 'Time Slot'],
                'table_rows':[
                ]     
            }
        reservations= FieldReservation.objects.all()    
        for reservation in reservations:  
            tableOptions['table_rows'].append([reservation.date,reservation.slot_time])
        table = Component('table',tableOptions).create()    
        return render(request,'system/form.html',{'title':title,'form':discountMessage+form+table})
    else:
        messages.error(request,'You must Login to Reserve the Field')
        return redirect('/')
def reservationValidate(request):
    if (request.method== 'POST'):
        requestData= request.POST.copy()
        try:
            existingReservation= FieldReservation.objects.filter(date= requestData['date'], slot_time=requestData['slot_time']).first()
            
        except:
            existingReservation= None
        if (existingReservation is None):
            reservationCost = 15
            user = User.objects.filter(email=request.session['login']['email']).first()
            discount = Discounts.objects.filter(fan_tier=user.fan_tier).first()
            totalCharge = reservationCost*(100-discount.discount)/100
            AccountSummary.objects.create(user=user,transaction_name="Reservation "+ requestData['date']+ " "+requestData['slot_time'],transaction_amount=totalCharge)
            FieldReservation.objects.create(date= requestData['date'], slot_time=requestData['slot_time'],user=user)
            messages.success(request,'Reservation Successful, Price: 15$')
        else:
            messages.error(request,'Time slot reserved')
    return redirect('/fieldReservation')
