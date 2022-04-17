from django.urls import path
import system.domains.Reports.ReportsController as views


urlpatterns = [
    path('selectMatch/', views.selectMatch),
    path('renderMatch/<int:id>', views.renderMatch),
    path('selectDate/', views.selectDate),
    path('financialSummary/', views.financialSummary),
    
]