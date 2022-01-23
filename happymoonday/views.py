from django.shortcuts import render, redirect
from .models import Customer, Sales
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def index(request):
    isSales = Sales.objects.all().exists()
    isCustomer = Customer.objects.all().exists()

    return render(request, 'happymoonday/index.html', {"dataExist":isSales and isCustomer})


def rate(request):
    products_list = Sales.objects.all().values('product').distinct()
    sales_list = Sales.objects.all().values('email', 'product', 'count', 'date')
    age_product_list = {}
    sum_by_product={}
    sum_by_age={10:0, 20:0, 30:0, 40:0, 50:0}
    
    for productList in products_list:
        productName = productList['product']
        age_product_list[productName.replace(' ', '_')]={10: 0, 20: 0, 30: 0, 40: 0, 50: 0}
        sum_by_product[productName.replace(' ', '_')]=0

    for salesList in sales_list:
        try:
            salesCustomerInfo = Customer.objects.get(email=salesList['email'])
            age = int((salesList['date'].year - salesCustomerInfo.birth.year)/10)*10
            productName = salesList['product'].replace(' ', '_')
            if age>50:
                age=50
            age_product_list[productName][age]=age_product_list[productName][age]+salesList['count']
            sum_by_product[productName]=sum_by_product[productName]+salesList['count']
            sum_by_age[age]=sum_by_age[age]+salesList['count']
        except Customer.DoesNotExist:
            salesCustomerInfo=None

    return render(request, 'happymoonday/saledRate.html', {'product_list': age_product_list, 'customer':sales_list, 'sumByProduct':sum_by_product, 'sumByAge':sum_by_age})


# def comparison(request):
#     salesInfo = Sales.objects.filter(date__year=2021)
#     weekly_sum = {}
#     for item in salesInfo:
#         weekly_number = item.date.isocalendar()[0], '_', item.date.isocalendar()[1], '주차'
#         weekly_sum[weekly_number]=0
#         print(weekly_sum[weekly_number])

#     return render(request, 'happymoonday/salesComparison.html', {'product_list': salesInfo})

def comparison (request):
    # 그래프에 한글 출력시 폰트 변경 (기본폰트 : sans-serif)
    matplotlib.rcParams['font.family'] = 'Malgun Gothic'
    # 그래프에서 마이너스(-)폰트 깨짐 방지
    matplotlib.rcParams['axes.unicode_minus'] = False

    # 멤버 이름
    member_name = ['A','B','C','D']
    # 막대 그래프 너비값
    bar_width = 0.4
    # 운동 전 데이터
    before_data = [56,70,46,90]
    # 운동 후 데이터
    after_data = [70,75,60,100]
    # x축 데이터 [0,1,2,3]
    index = np.arange(len(member_name))

    # before 막대 그래프
    plt.bar(index, before_data, color = 'r', align='edge', width=bar_width, label='before')
    # after 막대 그래프
    plt.bar(index + bar_width, after_data, color = 'c', align='edge', width=bar_width, label='after')

    # after 막대 그래프 x축 데이터에 맞춰 라벨 지정
    plt.xticks(index + bar_width, member_name)
    # plt.bar(label='문자열')을 통해 범례지정
    plt.legend()
    # x축 라벨 
    plt.xlabel('회원 이름')
    # y축 라벨
    plt.ylabel('팔굽혀펴기 횟수')
    # 타이틀
    plt.title('운동 시작 전과 후 비교')
    plt.show()


    return render(request, 'happymoonday/salesComparison.html', {'graphic':graphic})

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

    return render(request, 'happymoonday/index.html', {"dataExist":True})

"""
rows = filter.values(product).distinct()
프로덕트 목록

1. sales 목록 불러옴
2. 해당 행의 email로 customer 불러옴(필터링)
3. 불러온 customer의 birth로 나이대 계산하기
4. 나이대별 정리가능한 array에 삽입

나이별 총합 array
상품별 총합 array

product
int(나이 / 10))  <- 나이대

"""

"""
1. 상품별로 매출일 불러옴
"""