#coding=utf-8
from django.db import models
from df_user.models import UserInfo
from df_goods.models import GoodsInfo

# Create your models here.
class CartInfo(models.Model):
    user=models.ForeignKey('df_user.UserInfo',on_delete=models.CASCADE)
    goods=models.ForeignKey('df_goods.GoodsInfo',on_delete=models.CASCADE)
    count=models.IntegerField()
