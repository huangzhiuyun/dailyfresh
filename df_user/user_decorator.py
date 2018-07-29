# coding=utf-8
from django.http import HttpResponseRedirect

# 验证登录，如果未登录，就转到登录页面。
def login_fun(func):
    def login_func(request,*args,**kwargs):
        if request.session.has_key('user_id'):      #判断session中有该用户，回到装饰器装饰的func
            return func(request,*args,**kwargs)     #兼容之后的参数传递
        else:
            red=HttpResponseRedirect('/user/login/')
            red.set_cookie('url',request.get_full_path())
            return red
    return login_func

'''
http://127.0.0.1:8080/200/?type=10
request.path():表示当前路径,为/200/
request.get_full_path():表示完整路径/200/?type=10
'''










