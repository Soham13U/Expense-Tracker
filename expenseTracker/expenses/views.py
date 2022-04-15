from curses.ascii import HT
from pickle import FALSE
from re import template
import tempfile
from unittest import result
from urllib import response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense,Budget
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse,HttpResponse
from userpreferences.models import UserPreference
import datetime
from django.core.paginator import Paginator
import csv
import xlwt

from django.template.loader import render_to_string
import os

#from weasyprint import HTML
import tempfile
from django.db.models import Sum
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from datetime import timedelta
from django.utils.timezone import localtime
from django.db.models import Sum




from .models import Category

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    categories=Category.objects.all()
    expenses=Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses,5)
    page_number =request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    today_date_time = localtime()
    today_date = datetime.date.today()
    # budget=0
    spent =0
    exists = UserPreference.objects.filter(user=request.user).exists()
    exists2= Budget.objects.filter(user=request.user).exists()
    exists3= Expense.objects.filter(owner=request.user).exists()
   
    if exists:
            currency = UserPreference.objects.get(user = request.user).currency
            
    else:
            currency = 'INR - Indian Rupee'

    if exists2:
        budget= Budget.objects.get(user = request.user).budget
    else:
        Budget.objects.create(user=request.user,budget=0)

    


    

    budget = request.POST.get('budget',0)

    if  budget:
        
        Budget.objects.filter(user=request.user).update(budget=budget)
        budget = Budget.objects.get(user=request.user).budget
        messages.success(request, 'Budget updated')
    else:
        budget = Budget.objects.get(user=request.user).budget

    
   
    expenses_year = Expense.objects.filter(owner=request.user,date__year=today_date.year)
    expenses_month = expenses_year.filter(date__month=today_date.month)
    spent_month = expenses_month.aggregate(Sum('amount'))
    if not spent_month['amount__sum']:
        spent_month['amount__sum'] = 0.0

    if   spent_month['amount__sum'] > budget:
        messages.error(request,'Budget limit exceeded') 

    
    remaining = float(budget) - float( spent_month['amount__sum'])
    mdate = datetime.date.today()
    month = mdate.strftime("%B")
    

    context={
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency,
        'budget':budget,
        'spent_month':spent_month['amount__sum'],
        'remaining':remaining,
        'month':month
         
    }
    return render(request,'expenses/index.html',context)

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

        if not amount.isnumeric():
            messages.error(request, 'Amount should be a number')
            return render(request, 'expenses/add_expense.html', context)

        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense added successfully')

        return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)

        if not amount.replace('.','',1).isdigit():
            messages.error(request, 'Amount should be a number')
            return render(request, 'expenses/edit-expense.html', context)

        

        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated successfully')

        return redirect('expenses')

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/statsExpense.html')

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Expenses' + str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])

    expenses= Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])

    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Expenses' + str(datetime.datetime.now()) + '.xls'
    wb= xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount','Description','Category','Date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style = xlwt.XFStyle()

    rows= Expense.objects.filter(owner=request.user).values_list('amount','description','category','date')

    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
         ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)
    return response

def export_pdf(request):
    template_path='expenses/pdf-e.html'
    expenses=Expense.objects.filter(owner=request.user)
    currency = UserPreference.objects.get(user = request.user).currency
    context={'expenses':expenses,
    'currency':currency}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename=Expenses' + str(datetime.datetime.now()) + '.pdf'
    template=get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse('Error')

  
    return response

def bdata(request):
#    if request.method =='POST':
   
       budget = request.POST.get('budget',False)
       Budget.objects.filter(user=request.user).update(budget=budget)
    #    add_b = Budget(user=request.user,budget=budget)
    #    add_b.budget = budget
    #    add_b.save()
       context={'budget':budget}
       messages.success(request, 'Budget updated')
       
       return render(request,'expenses/index.html',context)
    #    return redirect('expenses')