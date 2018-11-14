#!/usr/bin/env python  
# encoding: utf-8 

""" 
@version: v1.0 
@author: Shijie Qin 
@license: Apache Licence  
@contact: qsj4work@gmail.com
@site: https://shijieqin.github.io 
@software: PyCharm 
@file: xmlrpc.py 
@time: 2018/11/8 3:16 PM 
"""
import xmlrpc.client


class XmlRpc:
    @staticmethod
    def connection(host, port, username, password):
        if username == "" and password == "":
            address = "http://{0}:{1}/RPC2".format(host, port)
        else:
            address = "http://{0}:{1}@{2}:{3}/RPC2".format(
                username, password, host, port
            )

        try:
            return xmlrpc.client.ServerProxy(address)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def is_connected(connection):
        if connection:
            try:
                connection.system.listMethods()
                return 0
            except (xmlrpc.client.ProtocolError, xmlrpc.client.Fault) as err:
                print(err)
                return -1
            except Exception as err:
                print(err)
                return -1
        return -1
