from django.shortcuts import render, redirect
from .models import Customer, Sales
from matplotlib import pyplot
import numpy


def index(request):
    isSales = Sales.objects.all().exists()
    isCustomer = Customer.objects.all().exists()

    return render(request, 'happymoonday/index.html', {"dataExist":isSales and isCustomer})


def rate(request):
    products_list = Sales.objects.all().values('product').distinct()
    sales_list = Sales.objects.all().values('email', 'product', 'count', 'date')
    age_product_list = {}
    product_age_list = {10:{}, 20:{}, 30:{}, 40:{}, 50:{}}
    sum_by_product={}
    sum_by_age={10:0, 20:0, 30:0, 40:0, 50:0}
    
    for productList in products_list:
        productName = productList['product']
        age_product_list[productName.replace(' ', '_')]={10: 0, 20: 0, 30: 0, 40: 0, 50: 0}
        product_age_list[10][productName.replace(' ', '_')]=0
        product_age_list[20][productName.replace(' ', '_')]=0
        product_age_list[30][productName.replace(' ', '_')]=0
        product_age_list[40][productName.replace(' ', '_')]=0
        product_age_list[50][productName.replace(' ', '_')]=0
        sum_by_product[productName.replace(' ', '_')]=0


    for salesList in sales_list:
        try:
            salesCustomerInfo = Customer.objects.get(email=salesList['email'])
            age = int((salesList['date'].year - salesCustomerInfo.birth.year)/10)*10
            productName = salesList['product'].replace(' ', '_')
            if age>50:
                age=50
            age_product_list[productName][age]=age_product_list[productName][age]+salesList['count']
            product_age_list[age][productName]=product_age_list[age][productName]+salesList['count']
            sum_by_product[productName]=sum_by_product[productName]+salesList['count']
            sum_by_age[age]=sum_by_age[age]+salesList['count']
        except Customer.DoesNotExist:
            salesCustomerInfo=None

    return render(request, 'happymoonday/saledRate.html', {'product_list': age_product_list,'age_product_list':product_age_list, 'customer':sales_list, 'sumByProduct':sum_by_product, 'sumByAge':sum_by_age})


def comparison(request):
    salesInfo = Sales.objects.all()
    weekly_sum = {}
    label=[]
    weekday=[]
    weekend=[]

    for item in salesInfo:
        weekly_number = "{}_{}".format(item.date.isocalendar()[0],item.date.isocalendar()[1] )
        if weekly_sum.__contains__(weekly_number)==False:
            weekly_sum[weekly_number]={"weekday":0, "weekend":0}
        
        if 1<=item.date.isocalendar()[2]<=5:
            weekly_sum[weekly_number]["weekday"]=weekly_sum[weekly_number]["weekday"]+item.count
        else :
            weekly_sum[weekly_number]["weekend"]=weekly_sum[weekly_number]["weekend"]+item.count

    for item in weekly_sum:
        label.append(item);
        weekday.append(weekly_sum[item]["weekday"]/5);
        weekend.append(weekly_sum[item]["weekend"]/2);


    pyplot.rcParams["font.size"] = 12
    pyplot.rcParams["figure.figsize"] = (12, 8)
    
    pyplot.figure(facecolor='#f4f1ed')

    x = numpy.arange(len(label))
    pyplot.bar(x-0.0, weekday, label='Weekday', width=0.2, color='#C5875D')
    pyplot.bar(x+0.2, weekend, label='Weekend', width=0.2, color='#CCA69C')
    pyplot.xticks(x, label)

    pyplot.legend()
    pyplot.xlabel('Week number')
    pyplot.ylabel('Day avarage count')
    pyplot.title('Compare between weekday and weekend')

    
    pyplot.savefig('happymoonday/static/graph.png', bbox_inches='tight', pad_inches=0)

    pyplot.close()

    return render(request, 'happymoonday/salesComparison.html', {'dataExists': salesInfo.exists()})


def dataAdd(request):
    isSales = Sales.objects.all().exists()
    isCustomer = Customer.objects.all().exists()
    ## customer insert
    if isCustomer==False:
        Customer.objects.create(email='dahee1@gmail.com', birth='2002-05-22')
        Customer.objects.create(email='dahee2@gmail.com', birth='1970-07-15')
        Customer.objects.create(email='dahee3@gmail.com', birth='1990-08-15')
        Customer.objects.create(email='dahee4@gmail.com', birth='1988-06-06')
        Customer.objects.create(email='dahee5@gmail.com', birth='1985-03-01')
        Customer.objects.create(email='dahee6@gmail.com', birth='1997-01-01')
        Customer.objects.create(email='dahee7@gmail.com', birth='1991-10-03')
        Customer.objects.create(email='dahee8@gmail.com', birth='1978-05-05')
        Customer.objects.create(email='dahee9@gmail.com', birth='2005-07-10')
        Customer.objects.create(email='dahee10@gmail.com', birth='1999-12-25')

    ## sales insert
    if isSales==False:
        Sales.objects.create(email='dahee1@gmail.com', product='생리대 중형', count=1, date='2022-01-01')
        Sales.objects.create(email='dahee2@gmail.com', product='생리대 대형', count=4, date='2022-01-02')
        Sales.objects.create(email='dahee3@gmail.com', product='탐폰 라이트', count=3, date='2022-01-03')
        Sales.objects.create(email='dahee4@gmail.com', product='탐폰 레귤러', count=5, date='2022-01-04')
        Sales.objects.create(email='dahee5@gmail.com', product='탐폰 슈퍼', count=1, date='2022-01-05')
        Sales.objects.create(email='dahee6@gmail.com', product='생리대 중형', count=1, date='2022-01-06')
        Sales.objects.create(email='dahee7@gmail.com', product='생리대 대형', count=2, date='2022-01-07')
        Sales.objects.create(email='dahee8@gmail.com', product='탐폰 라이트', count=3, date='2022-01-08')
        Sales.objects.create(email='dahee1@gmail.com', product='탐폰 레귤러', count=3, date='2022-01-09')
        Sales.objects.create(email='dahee2@gmail.com', product='탐폰 슈퍼', count=2, date='2022-01-10')
        Sales.objects.create(email='dahee3@gmail.com', product='생리대 중형', count=5, date='2022-01-11')
        Sales.objects.create(email='dahee5@gmail.com', product='생리대 대형', count=4, date='2022-01-12')
        Sales.objects.create(email='dahee7@gmail.com', product='탐폰 라이트', count=1, date='2022-01-13')
        Sales.objects.create(email='dahee2@gmail.com', product='탐폰 레귤러', count=2, date='2022-01-14')
        Sales.objects.create(email='dahee8@gmail.com', product='탐폰 슈퍼', count=1, date='2022-01-15')
        Sales.objects.create(email='dahee5@gmail.com', product='생리대 중형', count=3, date='2022-01-16')
        Sales.objects.create(email='dahee2@gmail.com', product='생리대 대형', count=1, date='2022-01-17')
        Sales.objects.create(email='dahee1@gmail.com', product='탐폰 라이트', count=2, date='2022-01-18')
        Sales.objects.create(email='dahee5@gmail.com', product='탐폰 레귤러', count=2, date='2022-01-19')
        Sales.objects.create(email='dahee3@gmail.com', product='탐폰 슈퍼', count=3, date='2022-01-20')
        Sales.objects.create(email='dahee6@gmail.com', product='생리대 중형', count=1, date='2022-01-21')
        Sales.objects.create(email='dahee4@gmail.com', product='생리대 대형', count=6, date='2022-01-22')
        Sales.objects.create(email='dahee2@gmail.com', product='탐폰 라이트', count=3, date='2022-01-23')
        Sales.objects.create(email='dahee1@gmail.com', product='탐폰 레귤러', count=1, date='2022-01-24')
        Sales.objects.create(email='dahee5@gmail.com', product='탐폰 슈퍼', count=5, date='2022-01-25')
        Sales.objects.create(email='dahee7@gmail.com', product='생리대 중형', count=2, date='2022-01-26')
        Sales.objects.create(email='dahee3@gmail.com', product='생리대 대형', count=4, date='2022-01-27')
        Sales.objects.create(email='dahee6@gmail.com', product='탐폰 라이트', count=1, date='2022-01-28')
        Sales.objects.create(email='dahee3@gmail.com', product='탐폰 레귤러', count=6, date='2022-01-29')
        Sales.objects.create(email='dahee2@gmail.com', product='탐폰 슈퍼', count=2, date='2022-01-30')
        Sales.objects.create(email='dahee9@gmail.com', product='생리대 중형', count=5, date='2022-02-01')
        Sales.objects.create(email='dahee9@gmail.com', product='생리대 대형', count=5, date='2022-02-02')
        Sales.objects.create(email='dahee9@gmail.com', product='탐폰 라이트', count=1, date='2022-01-28')
        Sales.objects.create(email='dahee8@gmail.com', product='탐폰 레귤러', count=6, date='2022-01-29')
        Sales.objects.create(email='dahe6@gmail.com', product='탐폰 슈퍼', count=2, date='2022-01-30')
        Sales.objects.create(email='dahee10@gmail.com', product='탐폰 라이트', count=4, date='2022-01-12')

    return render(request, 'happymoonday/index.html', {"dataExist":True})
