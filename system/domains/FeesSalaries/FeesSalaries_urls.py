from django.urls import path
import system.domains.FeesSalaries.FeesSalariesController as views


urlpatterns = [
    path('manageFeesSalaries/', views.manageFeesSalaries),# render the monthly fees/salaries for all roles and tiers
    path('deleteFeesSalaries/<int:id>', views.deleteFeesSalaries),# delete a fee/salary for a role-tier combination
    path('CreateFeesSalaries/', views.CreateFeesSalaries),# create a fee/salary for a given role-tier combination
    path('feesSalariesValidate/', views.feesSalariesValidate),# validate the created salary
    path('feesSalariesSubmit/', views.feesSalariesSubmit),# submit the fees and salaries to the users account summaries
    path('feesSalariesRollback/', views.feesSalariesRollback),#rollback the fees and salaries if submitted by accident
]