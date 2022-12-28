from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .models import Profile, Addmoney, TotalBudget
from django.contrib import messages
from datetime import date
import math
# Create your views here.

#  for Home Screen 
def home(request):
    color = False
    
    total_bud_data = TotalBudget.objects.all()
    

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
        totalBudgetData = total_bud_data.values('total_bud')[0]['total_bud']
    # print(f"{type(balanceData)} --  {balanceData}")
        # print(f"{type(totalBudgetData)} --  {totalBudgetData}")
    if budgetData == 0:
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
    check = False
    name =''
    current_bal = ''
    current_bud = ''
    if request.method == 'POST':
        total_bud = ''
        name = request.POST['nameData']
        current_bal = request.POST['balanceData']
        current_bud = request.POST['budgetData']
        total_bud = request.POST['budgetData']
        # print(name)
        form_bud = TotalBudget(total_bud=total_bud)
        form_bud.save()

        print(f"{type(total_bud)}--{total_bud}")
        print(type(current_bal))
        # print(current_bud)
        form_Profile = Profile(user=name, current_balance=current_bal, budget=current_bud)
        form_Profile.save()
    
    ProData = Profile.objects.all()

    # data = Profile.objects.values()

    if len(ProData) == 0:
        name =''
        current_bal = ''
        current_bud = ''
    else:

        name = ProData.values('user')[0]['user']
        current_bal = ProData.values('current_balance')[0]['current_balance']
        current_bud = ProData.values('budget')[0]['budget']

    context = {
        'ProData' : ProData,
        'name'     : name,
        'current_bal' :current_bal,
        'current_bud' :current_bud
    
    }
    return render(request, 'ExpenseApp/profile_Screen.html',context=context)


# Show Transaction screen 
def showTransactionList(request):

    # using "-" this we can get latest records from the DataBase
    transData = Addmoney.objects.order_by("-transDate") 
    dataList = []
    # Pagination logic
    pagiPerPageCount = 4
    curPage = 1
    lastPage = ''
    pageNum = []
    currentPage = request.GET.get('page')

    #  converting request  data in int 
    #  checking page number should not be nun and 
    #  it be numeric number or not 

    if currentPage is not None and currentPage.isnumeric():
        curPage = int(currentPage)
    
    
    lenData = len(transData)
    pageCount = math.ceil(lenData/pagiPerPageCount)
    startPoint = (curPage -1)*pagiPerPageCount
    endpoint = startPoint+pagiPerPageCount
    dataList = transData[startPoint:endpoint]

    #  for printing page number converting integer into list
    for pa in range(1,pageCount+1):
        pageNum.append(pa)

    #  for last page
    if len(pageNum) == 0:
        lastPage = '0'
    else:
        lastPage = pageNum[-1]
    # print(f"last page number list -- {lastPage} ")
    # print(f"{type(curPage)}---{curPage}")
    # print(f"{type(pageCount)}--{pageCount}")
    # print(f"{type(startPoint)}--{startPoint}")
    # print(f"{type(endpoint)}---{endpoint}")
    dataAnalysis(request)

    # print(transData)
    context = {
        "TransData" : dataList,
        "pageCount" : pageNum,
        "lastPage"  : lastPage
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
        if len(dateTime) == 0:
            dateTime = date.today()
        transType = request.POST['transType']
        transDisc = request.POST['transDisc']
        if len(transDisc) == 0:
            transDisc = "Others"
        quantity = request.POST["quantity"]
        if transType == exp:
            balance = float(balData) - float(quantity)
            budg = float(budData) - float(quantity) 
        else :
            balance = float(balData) + float(quantity)
            budg = budData
        
        if proData.filter(user=userData).exists():
            objects = Profile.objects.filter(user=userData)
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


def dataAnalysis(request):
    # catData = ''
    catPrice = []
    catItem = 'Food'
    catList = ['Food','Travel','Shopping','Groceries','Entertainment','Necessities','Other']
    transData = Addmoney.objects.filter(transType="Expense")
    print(transData)
    print(catItem in catList)
    if catItem in catList:
        catData = transData.filter(catData=catItem).values('quantity')
        for price in catData:
            print(f"{type(price)}---{price}")
