from django.db import models

# Create your models here.

class Customer(models.Model): #table 이름
    email = models.CharField(max_length = 200, primary_key=True) #Field
    birth = models.DateField() #Field

    class Meta:
        db_table = "customer"
    
    def __str__(self):
        return self.email

class Sales(models.Model):
    PRODUCT_TYPE = (
        ('생리대 중형', '생리대 중형'),
        ('생리대 대형', '생리대 대형'),
        ('탐폰 라이트', '탐폰 라이트'),
        ('탐폰 레귤러', '탐폰 레귤러'),
        ('탐폰 슈퍼', '탐폰 슈퍼'),
    )
    email = models.CharField(max_length = 200)
    product = models.CharField(max_length = 200, choices=PRODUCT_TYPE)
    count = models.IntegerField(default=0)
    date = models.DateField()

    class Meta:
        db_table = "sales"

    def __str__(self):
        return self.email+' - '+ self.product

