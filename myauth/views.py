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
                result = {'msg': 'login success', 'code': '0'}
            else:
                result = {'msg': 'login faild', 'code': '-1'}
        except:
            result = {'msg': 'login faild', 'code': '-1'}
        return JsonResponse(result)
    return render(request, 'myauth/login.html')


def logout(request):
    Flatfish.delInstance(request.user)
    auth.logout(request)
    return HttpResponseRedirect(
        reverse('myauth:login')
    )