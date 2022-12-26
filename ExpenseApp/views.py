from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .models import Profile, Addmoney
from django.contrib import messages
# Create your views here.

#  for Home Screen 
def home(request):
    context = {}
    transData = Addmoney.objects.all()
    profile = Profile.objects.all()
    budgetData = profile.values('budget')
    balanceData =  profile.values('current_balance')
    transType = transData.values('transType')
    quantity = transData.values('quantity')
    if transType == 'Expense':
        budgetData = budgetData - quantity
        balanceData = balanceData - quantity

    trans_context = {
        "budgetData" : budgetData,
        "balanceData" : balanceData
    }
    return render(request, 'ExpenseApp/Home.html', trans_context)

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
    data = Profile.objects.values()
    context = {'ProData' : data}
    return render(request, 'ExpenseApp/profile_Screen.html',context=context)


# Show Transaction screen 
def showTransactionList(request):
    transData = Addmoney.objects.all()
    lenData = len(transData)
    context = {
        "TransData" : transData,
        "numData" : range(1, lenData +1)
        }
    return render(request, 'ExpenseApp/show_transaction.html', context)


# Add transactions 
def addTransaction(request):
    context = {}
    if request.method == 'POST':
        category = request.POST['catData']
        dateTime = request.POST['dateTime']
        transType = request.POST['transType']
        transDisc = request.POST['transDisc']
        quantity = request.POST["quantity"]
        trans_form = Addmoney(
            transType = transType,
            quantity = quantity,
            transDate = dateTime,
            catData = category,
            transDisc = transDisc
        )
        
        trans_form.save()
        messages.success(request, "Added Transaction List !!!")
    data = Addmoney.objects.values()
    print(Addmoney.objects.all().values_list())
    context={
        "TransData" : data,
    }
    return render(request, 'ExpenseApp/add_transaction.html',context=context)


