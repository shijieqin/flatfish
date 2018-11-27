from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from core.flatfish import Flatfish
from django.contrib import auth

from django.contrib.auth.models import User


def login(request):
    result = {'msg': 'not login', 'code': '-1'}
    if request.user.is_authenticated:
        return HttpResponseRedirect(
            reverse('supervisor:home')
        )
    if request.method == "POST":
        print(request.body)
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                result = {'msg': '登录成功', 'code': '0'}
            else:
                result = {'msg': '用户名密码错误', 'code': '-1'}
        except:
            result = {'msg': '系统异常', 'code': '-1'}
        return JsonResponse(result)
    return render(request, 'myauth/login.html')


def change_password(request):
    result = {'msg': '修改失败', 'code': '-1'}
    if request.method == "POST":
        print(request.body)
        old_pwd = request.POST['old_pwd']
        new_pwd = request.POST['new_pwd']
        confirm_pwd = request.POST['confirm_pwd']
        if new_pwd == confirm_pwd:
            if new_pwd != old_pwd:
                try:
                    user = auth.authenticate(username=request.user.username, password=old_pwd)
                    if user is not None and user.is_active:
                        user.set_password(new_pwd)
                        user.save()
                        auth.login(request, user)
                        result = {'msg': '修改成功', 'code': '0'}
                    else:
                        result = {'msg': '旧密码错误', 'code': '-1'}
                except:
                    result = {'msg': '系统异常', 'code': '-1'}
            else:
                result = {'msg': '新密码与旧密码相同', 'code': '-1'}
        else:
            result = {'msg': '两次密码输入不相符', 'code': '-1'}
        return JsonResponse(result)

def logout(request):
    Flatfish.delInstance(request.user)
    auth.logout(request)
    return HttpResponseRedirect(
        reverse('myauth:login')
    )