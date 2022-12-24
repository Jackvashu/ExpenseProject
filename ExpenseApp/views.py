from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile
# Create your views here.

#  for Home Screen 
def home(request):
    return render(request, 'ExpenseApp/Home.html')

# for add profile details
def addProfile(request):
    context = {}
    if request.method == 'POST':
        
        name = request.POST['nameData']
        current_bal = request.POST['balanceData']
        current_bud = request.POST['budgetData']
        print(name)
        print(current_bal)
        print(current_bud)
        form_Profile = Profile(user=name, current_balance=current_bal, budget=current_bud)
        form_Profile.save()
    
    profile_Data = Profile.objects.all()
    print(profile_Data.values())
    context = {'ProData' : profile_Data.values()}
    return render(request, 'ExpenseApp/profile_Screen.html',context=context)


# Show Transaction screen 
def showTransactionList(request):
    return render(request, 'ExpenseApp/show_transaction.html')


# Add transactions 
def addTransaction(request):
    return render(request, 'ExpenseApp/add_transaction.html')


