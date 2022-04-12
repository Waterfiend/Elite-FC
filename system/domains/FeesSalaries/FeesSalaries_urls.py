from django.urls import path
import system.domains.FeesSalaries.FeesSalariesController as views


urlpatterns = [
    path('manageFeesSalaries/', views.manageFeesSalaries),
    path('deleteFeesSalaries/<int:id>', views.deleteFeesSalaries),
    path('CreateFeesSalaries/', views.CreateFeesSalaries),
    path('feesSalariesValidate/', views.feesSalariesValidate),
    path('feesSalariesSubmit/', views.feesSalariesSubmit),
    path('feesSalariesRollback/', views.feesSalariesRollback),
]