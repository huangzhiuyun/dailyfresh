#coding=utf-8
from django.db import models


# Create your models here
class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('df_user.UserInfo', on_delete=models.CASCADE)
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=7, decimal_places=2)  # 总价
    oaddress = models.CharField(max_length=150, default='')
    zhifu = models.IntegerField(default=0)     #暂无支付接口，未实现
    owuliu = models.CharField(max_length=200)   #暂无物流查询链接窗口，未实现

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()
