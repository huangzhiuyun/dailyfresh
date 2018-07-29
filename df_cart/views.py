# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render, redirect
from df_user.user_decorator import login_fun
from df_cart.models import CartInfo
from df_goods.models import *


# Create your views here.
@login_fun
def cart(request):
    uid = request.session['user_id']  # 当前登录的用户
    carts = CartInfo.objects.filter(user_id=uid)  # 用该用户的id去购物车表中查他（她）所有的购物车信息
    context = {
        'title': '购物车',
        'carts': carts,
    }
    return render(request, 'df_cart/cart.html', context)


@login_fun
def add(request, gid, count):
    if int(gid) == 0 and request.is_ajax() and int(count) == 0:
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count': count})
    # 获取当前登录用户的ID
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # 查询购物车是否已有该商品，如果有这增加其数量，没有则增加一个新的商品
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    # 如果是ajax请求，则返回json，否则转向购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()  # 插查询当前登录用户购物车的商品类型总数量
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')  # 转向购物车


@login_fun
def edit(request, gid, count):
    try:
        if request.is_ajax():
            goods = CartInfo.objects.get(id=int(gid))
            goods.count = int(count)
            goods.save()
            data = {'ok': 1}
    except Exception as e:
        data = {'ok': int(count)}
    return JsonResponse(data)


@login_fun
def delete(request, gid):
    try:
        if request.is_ajax():
            goods = CartInfo.objects.get(id=int(gid))
            goods.delete()
            data = {'ok': 1}
            print(1111)
    except Exception as e:
        data = {'ok': 0, 'e': e}
    return JsonResponse(data)

