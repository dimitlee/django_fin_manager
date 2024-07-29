from django.contrib import admin
from .models import Category, Transaction, ScheduledTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_default')
    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('category', 'user', 'description', 'sum')
    
    
@admin.register(ScheduledTransaction)
class ScheduledTransactionAdmin(admin.ModelAdmin):
    list_display = ('category', 'user', 'sum', 'frequency', 'weekday', 'monthday', 'year_date')