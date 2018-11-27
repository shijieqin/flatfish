#!/usr/bin/env python  
# encoding: utf-8 

""" 
@version: v1.0 
@author: Shijie Qin 
@license: Apache Licence  
@contact: qsj4work@gmail.com
@site: https://shijieqin.github.io 
@software: PyCharm 
@file: url.py 
@time: 2018/11/8 2:54 PM 
"""
from django.conf.urls import url

from . import views

app_name = 'myauth'

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'change_password', views.change_password, name='change_password'),
]