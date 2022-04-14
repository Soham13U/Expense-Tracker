from unicodedata import name
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.index,name="expenses"),
    path('add-expense',views.add_expense,name="add-expenses"),
    path('edit-expense/<int:id>',views.expense_edit,name="expense-edit"),
    path('expense-delete/<int:id>',views.delete_expense,name="expense-delete"),
    path('search-expenses',csrf_exempt(views.search_expenses),name="search_expenses"),
    path('expense_category_summary',views.expense_category_summary,name="expense_category_summary"),
    path('statsE',views.stats_view,name="statsE"),
    path('export_csv',views.export_csv,name="export_csv_e"),
    path('export_excel',views.export_excel,name="export_excel_e"),
    # path('addb',views.bdata,name="addb"),

    path('export_pdf',views.export_pdf,name="export_pdf_e")
]
