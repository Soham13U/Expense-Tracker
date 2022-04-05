from django.shortcuts import render, redirect
from expenses.models import  Category, Expense
from income.models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse,HttpResponse
import csv
import xlwt
import datetime
from datetime import timedelta
from django.utils.timezone import localtime
from django.db.models import Sum
# Create your views here.



@login_required(login_url='/authentication/login')
def index(request):
    today_date_time = localtime()
    today_date = datetime.date.today()
    week_date_time = today_date - timedelta(days=7) 
    start_today_data = today_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_today_data = today_date_time.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    incomes_today_display = UserIncome.objects.filter(owner=request.user,date__range=(start_today_data,end_today_data)).order_by('date')
    expenses_today_display = Expense.objects.filter(owner=request.user,date__range=(start_today_data,end_today_data)).order_by('date')

    
    expenses_year = Expense.objects.filter(owner=request.user,date__year=today_date.year)
    expenses_month = expenses_year.filter(date__month=today_date.month)
    expenses_today = expenses_month.filter(date__exact=today_date)
    expenses_week = expenses_month.filter(date__gte=week_date_time)

    spent_year_count = expenses_year.count()
    spent_month_count = expenses_month.count()
    spent_today_count = expenses_today.count()
    spent_week_count = expenses_week.count()
    spent_month = expenses_month.aggregate(Sum('amount'))
    spend_today = expenses_today.aggregate(Sum('amount'))
    spent_week = expenses_week.aggregate(Sum('amount'))
    spent_year = expenses_year.aggregate(Sum('amount'))

    income_year = UserIncome.objects.filter(owner=request.user,date__year=today_date.year)
    income_month = income_year.filter(date__month=today_date.month)
    income_today = income_month.filter(date__exact=today_date)
    income_week = income_month.filter(date__gte=week_date_time)

    earned_year_count = income_year.count()
    earned_month_count = income_month.count()
    earned_today_count = income_today.count()
    earned_week_count = income_week.count()
    earned_month = income_month.aggregate(Sum('amount'))
    earned_today = income_today.aggregate(Sum('amount'))
    earned_week = income_week.aggregate(Sum('amount'))
    earned_year = income_year.aggregate(Sum('amount'))
    final={
       'val':[spent_year,earned_year]
   }


    return render(request, 'dashboard/index.html',{ 'expenses':expenses_today_display[:5],
        'incomes':incomes_today_display[:5],
        'spent_today':spend_today['amount__sum'],
        'spent_today_count':spent_today_count,
        'spent_month':spent_month['amount__sum'],
        'spent_month_count':spent_month_count,
        'spent_year':spent_year['amount__sum'],
        'spent_year_count':spent_year_count,
        'spent_week':spent_week['amount__sum'],
        'spent_week_count':spent_week_count,

        
        'earned_today':earned_today['amount__sum'],
        'earned_today_count':earned_today_count,
        'earned_month':earned_month['amount__sum'],
        'earned_month_count':earned_month_count,
        'earned_year':earned_year['amount__sum'],
        'earned_year_count':earned_year_count,
        'earned_week':earned_week['amount__sum'],
        'earned_week_count':earned_week_count,
        'val':[spent_year,earned_year]})


# @login_required(login_url='/authentication/login')
# def both_data(request):
#    incomes = UserIncome.objects.filter(owner=request.user)
#    expenses = Expense.objects.filter(owner=request.user)

#    today_date_time = localtime()
#    today_date = datetime.date.today()
#    week_date_time = today_date - timedelta(days=7) 
#    start_today_data = today_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
#    end_today_data = today_date_time.replace(hour=23, minute=59, second=59, microsecond=999999)

#    expenses_year = Expense.objects.filter(owner=request.user,date__year=today_date.year)
#    spent_year = expenses_year.aggregate(Sum('amount'))

#    income_year = UserIncome.objects.filter(owner=request.user,date__year=today_date.year)
#    earned_year = income_year.aggregate(Sum('amount'))
#    final={
#        'val':[spent_year,earned_year]
#    }


#    return render(request, 'dashboard/index.html',context=final)