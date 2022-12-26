from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .models import Profile, Addmoney
from django.contrib import messages
# Create your views here.

#  for Home Screen 
def home(request):
    color = False
    
    transData = Addmoney.objects.all() 
    latestData = transData.order_by("-transDate")[:10]
    profile = Profile.objects.all()
    if len(profile) == 0:
        budgetData = 0
        balanceData = 0
        totalBudgetData = 0
    else:
        budgetData = profile.values('budget')[0]['budget']
        balanceData =  profile.values('current_balance')[0]['current_balance']
        totalBudgetData = profile.values('left_Budget')[0]['left_Budget']
    # print(f"{type(balanceData)} --  {balanceData}")
    # print(f"{type(budgetData)} --  {budgetData}")
    if len(budgetData) == 0:
        color = False
    elif int(budgetData) < 0:
        color = True
    else:
        color = False
    
    trans_context = {
        "budgetData" : budgetData,
        "balanceData" : balanceData,
        "TransData" : latestData,
        'left_Budget' : totalBudgetData,
        "color" : color
    }
    return render(request, 'ExpenseApp/Home.html', trans_context)

# for add profile details
def addProfile(request):
    context = {}
    dataFlag = True
    if request.method == 'POST':
        
        name = request.POST['nameData']
        current_bal = request.POST['balanceData']
        current_bud = request.POST['budgetData']
        total_bud = request.POST['budgetData']
        # print(name)
        # print(current_bal)
        # print(current_bud)
        form_Profile = Profile(user=name, current_balance=current_bal, budget=current_bud, left_Budget=total_bud)
        form_Profile.save()
    
    profile_Data = Profile.objects.all()
    data = Profile.objects.values()
    if len(data) == 0:
        dataFlag = False
    else:
        dataFlag = True
    context = {
        'ProData' : data,
        'dataFlag' : dataFlag
    
    }
    return render(request, 'ExpenseApp/profile_Screen.html',context=context)


# Show Transaction screen 
def showTransactionList(request):

    # using "-" this we can get latest records from the DataBase
    transData = Addmoney.objects.order_by("-transDate") 

    print(transData)
    context = {
        "TransData" : transData,
        }
    return render(request, 'ExpenseApp/show_transaction.html', context)


# Add transactions 
def addTransaction(request):
    quant = ''      # temperary variable for quantity
    balance = 0    # temp variable for balance
    budg = 0       # temp variable for budget
    context = {}
    exp = "Expense"
    inc = "Income" 
    proData = Profile.objects.all()
    if len(proData) == 0:
        budData = ''
        balData = ''
        userData = ''
    else:
        budData = proData.values('budget')[0]['budget']        # value in int for budget
        balData = proData.values('current_balance')[0]['current_balance']       #value in int for balance
        userData = proData.values('user')[0]['user']
    print(f"{type(userData)} --  {userData}")
    print(f"{type(budData)} --  {budData}")
    print(f"{type(balData)} --  {balData}")

    if request.method == 'POST':
        category = request.POST['catData']
        dateTime = request.POST['dateTime']
        transType = request.POST['transType']
        transDisc = request.POST['transDisc']
        quantity = request.POST["quantity"]
        if transType == exp:
            balance = int(balData) - int(quantity)
            budg = int(budData) - int(quantity) 
        else :
            balance = int(balData) + int(quantity)
            budg = budData
        
        objects = Profile.objects.filter(user='testing_1')
        for obj in objects:
            obj.current_balance = balance
            obj.budget = budg
            obj.save()
        # pro_form.save()
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
    quanData = data.filter

    # print(Addmoney.objects.all().values_list())
    context={
        "TransData" : data,
    }
    return render(request, 'ExpenseApp/add_transaction.html',context=context)


