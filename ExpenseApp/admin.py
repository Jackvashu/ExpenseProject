from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Profile, Addmoney, TotalBudget, Expenses)
class AppAdmin(admin.ModelAdmin):
    pass