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

app_name = 'supervisor'

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^node/$', views.node, name='node'),
    url(r'^node/detail/(?P<node_name>[^/]+)/$', views.node_detail, name='node_detail'),
    url(r'^node/detail/(?P<node_name>[^/]+)/processes.json$', views.node_detail_query, name='query_node_detail'),
    url(r'^node/add/$', views.add_node, name='add_node'),
    url(r'^node/nodes.json$', views.node_query, name='query_node'),
    url(r'^process/$', views.process, name='process'),
    url(r'^process/start$', views.process_start, name='process_start'),
    url(r'^process/stop$', views.process_stop, name='process_stop'),
    url(r'^process/restart$', views.process_restart, name='process_restart'),
    url(r'^process/logs/logs.json$', views.read_process_log, name='process_get_logs'),
    url(r'^type/$', views.type, name='type'),
    url(r'^type/detail/(?P<type_name>[^/]+)/$', views.type_detail, name='type_detail'),
    url(r'^type/detail/(?P<type_name>[^/]+)/processes.json$', views.type_detail_query, name='query_type_detail'),
    url(r'^type/types.json$', views.type_query, name='query_type'),
    url(r'^environment/$', views.environment, name='environment'),
    url(r'^environment/detail/(?P<environment_name>[^/]+)/$', views.environment_detail, name='environment_detail'),
    url(r'^environment/detail/(?P<environment_name>[^/]+)/processes.json$', views.environment_detail_query, name='environment_type_detail'),
    url(r'^environment/environments.json$', views.environment_query, name='query_environment')
]