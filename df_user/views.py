#coding=utf-8
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from df_user.models import *
from df_goods.models import *
from hashlib import sha1
from df_user.user_decorator import login_fun
from . import user_decorator

def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    #接受用户输入值
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')

    #验证用户密码
    if upwd!=upwd2:
        return redirect('/user/register/')

    # 密码加密
    sl=sha1()
    sl.update(upwd.encode("utf8"))
    upwd3=sl.hexdigest()

    #创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    #注册成功转登录页
    return redirect('/user/login/')

def register_exist(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    #接受请求信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    #根据用户名查询对象
    users=UserInfo.objects.filter(uname=uname)
    print('umame')
    #判断：如果未查到，则同户名错误，如果查到则判断密码是否正确，正确者转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update(upwd.encode("utf8"))
        if s1.hexdigest()==users[0].upwd:
            url=request.COOKIES.get('url','/')  #登录成功之后，从COOKIES中取到这个登录前正在操作的url，
                                                # 跳转回到url页面，如果里面的url没有记录，就转到默认的‘/’首页
            red = HttpResponseRedirect(url)
            #记住用户名
            if jizhu !=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context={'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'de_user/login.html',context)
    else:
        context={'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

def logout(request):
    # request.session.flush()
    del request.session['user_name']
    del request.session['user_id']
    return redirect('/')

@login_fun
def info(request):
    user_info=UserInfo.objects.get(id=request.session['user_id'])
    # 最近浏览
    # goods_ids = request.COOKIES.get('good_ids','')
    # goods_ids1=goods_ids.split(',')
    # #GoodsInfo.objects.filter(id_in=goods_ids1) #没有按照用浏览的先后顺序排
    # goods_list=[]
    # for goods_id in goods_ids1:
    #     goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    goods_ids1 = request.session.get(str(request.session['user_id']), '')
    goods_list = []
    for goods_id in goods_ids1:
        goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context={
        'uphone':user_info.uphone,
        'usddress':user_info.uaddress,
        'title':'用户中心',
        'user_email':user_info.uemail,
        'user_name':request.session['user_name'],
        'goods_list':goods_list,
    }
    return render(request,'df_user/user_center_info.html',context)

@login_fun
def order(request):
    context={'title':'用户中心'}
    return render(request,'df_user/user_center_order.html',context)

@login_fun
def site(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()
    context={'title':'用户中心','user':user}
    return render(request,'df_user/user_center_site.html',context)
























