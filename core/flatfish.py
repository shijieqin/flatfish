#!/usr/bin/env python  
# encoding: utf-8 

""" 
@version: v1.0 
@author: Shijie Qin 
@license: Apache Licence  
@contact: qsj4work@gmail.com
@site: https://shijieqin.github.io 
@software: PyCharm 
@file: flatfish.py 
@time: 2018/11/8 4:17 PM 
"""
import json
import xmlrpc.client

from django.db.models import QuerySet
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404

from core.process import Process
from core.xmlrpc import XmlRpc
from supervisor.models import Node
from itertools import chain


class Flatfish:
    __instances = dict()

    def __init__(self, user):
        self.user = user
        self.__connections = dict()
        self.__nodes = None
        self.__policy = dict()
        self.load()

    @staticmethod
    def getInstance(user):
        """ Static access method """
        _instance = Flatfish.__instances.get(user.username)
        if _instance is None:
            _instance = Flatfish(user)
            Flatfish.__instances[user.username] = _instance
        return _instance

    @staticmethod
    def delInstance(user):
        _instance = Flatfish.__instances.get(user.username)
        if _instance is not None:
            Flatfish.__instances.pop(user.username)

    @property
    def connections(self):
        # if len(self.__connections) == 0:
        self.init_connections()
        return self.__connections

    @property
    def nodes(self):
        # if self.__nodes is None:
        self.init_nodes()
        return self.__nodes

    @property
    def policy(self):
        # if len(self.__policy) == 0:
        self.init_policy()
        return self.__policy

    def init_nodes(self):
        _nodes = Node.objects.none()
        if self.user.is_superuser:
            _nodes = Node.objects.all()
        else:
            for group in self.user.groups.all():
                _group_nodes = Node.objects.none()
                for policy in group.policy_set.all():
                    _policy_nodes = policy.nodes.all()
                    _group_nodes = _group_nodes | _policy_nodes
                _nodes = _nodes | _group_nodes

        self.__nodes = _nodes.distinct()

    def init_connections(self):
        _connections = dict()
        for node in self.nodes:
            _connection = node.generate_connection()
            _connections[node.name] = _connection
        self.__connections = _connections

    def init_policy(self):
        _policy = dict()
        _policy_environment = set()
        _policy_type = set()
        for group in self.user.groups.all():
            for policy in group.policy_set.all():
                for environment in policy.environment.lower().split(";"):
                    _policy_environment.add(environment)

                for type in policy.type.lower().split(";"):
                    _policy_type.add(type)
        _policy["environment"] = list(_policy_environment)
        _policy["type"] = list(_policy_type)

        self.__policy = _policy

    def load(self):
        print("Loading")
        self.init_nodes()
        self.init_connections()
        self.init_policy()

    def reload(self):
        print("Reloading...")
        self.load()
        print("Reloaded.")

    @property
    def processes_tree(self):
        _processes_tree = dict()
        for node_name, _connection in self.connections.items():
            _processes = list()
            try:
                if XmlRpc.is_connected(_connection) == 0:
                    _processes_info = _connection.supervisor.getAllProcessInfo()
                    for _p in _processes_info:
                        _process = self.generate_process(_p, node_name)
                        if self.has_permistion(_process):
                            _processes.append(_process)
            except Exception as _:
                print(_)
            _processes_tree[node_name] = _processes
        return _processes_tree

    def generate_process(self, p, node_name):
        process = Process(p)
        process.dictionary["node"] = node_name
        process.dictionary["environment"] = self.__get_environment(process.name)
        process.dictionary['type'] = self.__get_type(process.name)
        return process

    @property
    def processes(self):
        _processes = list()
        for node_name, _process_list in self.processes_tree.items():
            _processes.extend(_process_list)
        return _processes

    def get_processes(self, process_name, node_names=None):
        _processes = list()
        if node_names is None:
            node_names = [_node.name for _node in self.nodes]

        for node_name in node_names:
            for _process in self.processes_tree.get(node_name):
                if _process.name == process_name:
                    _processes.append(_process)
        return _processes

    def get_processes_or_404(self, process_name, node_names=None):
        _processes = self.get_processes(process_name, node_names)
        if len(_processes) == 0:
            raise Http404('No %s matches the given query.' % process_name)
        return _processes

    @property
    def group_tree(self):
        _group_tree = dict()
        for p in self.processes:
            _group_tree[p.group] = _group_tree.get(p.group, dict())
            if p.node not in _group_tree[p.group]:
                _group_tree[p.group].append(p.node)

        return _group_tree

    def get_processes_by_group_name(self, group_name):
        return [p for p in self.processes if p.group == group_name]

    def get_processes_by_type_name(self, type):
        return [p for p in self.processes if p.type == type]

    def get_processes_by_environment_name(self, environment):
        return [p for p in self.processes if p.environment == environment]

    def get_node(self, node_name):
        return self.nodes.get(name=node_name)

    def get_node_or_404(self, node_name):
        node = self.get_node(node_name)
        if node:
            return node
        else:
            raise Http404('No %s matches the given query.' % node_name)

    @property
    def types(self):
        types = set()
        for p in self.processes:
            types.add(p.type)

        return list(types)

    @property
    def environments(self):
        environments = set()
        for p in self.processes:
            environments.add(p.environment)

        return list(environments)


    def get_environment_details(self, environment):
        environment = {
            "name": environment,
            "members": self.get_processes_by_environment(environment),
        }
        return environment

    def serialize_environments(self):
        environments_with_details = []
        for environment in self.environments:
            environment_detail = self.get_environment_details(environment)
            environments_with_details.append(environment_detail)

        return environments_with_details

    def __get_type(self, name):
        return name.split('-')[1].title()

    def __get_environment(self, name):
        return name.split('-')[0].title()

    def has_permistion(self, p):
        if(self.user.is_superuser):
            return True
        if (p.environment.lower() in self.policy.get('environment', list())
            or "*" in self.policy.get('environment', list())) \
                and (p.type.lower() in self.policy.get('type') or "*" in self.policy.get('type')):
            return True
        else:
            return False

    def get_process_logs(self, process_name, node_name):
        node = self.get_node_or_404(node_name)
        log_string = node.generate_connection().supervisor.tailProcessStdoutLog(
            process_name, 0, 30000
        )[0]
        log_list = log_string.split("\n")[1:-1]
        return log_list

    def start_process(self, process_name, node_name):
        """
            http://supervisord.org/api.html#supervisor.rpcinterface.SupervisorNamespaceRPCInterface.startProcess
        """
        process = self.get_processes_or_404(process_name, [node_name])[0]
        node = self.get_node_or_404(node_name)
        try:
            if node.generate_connection().supervisor.startProcess(process.name):
                return True, ""
            else:
                return False, "cannot start process"
        except xmlrpc.client.Fault as err:
            return False, err.faultString
        except Exception as err:
            return False, str(err)

    def stop_process(self, process_name, node_name):
        """
            http://supervisord.org/api.html#supervisor.rpcinterface.SupervisorNamespaceRPCInterface.startProcess
        """
        process = self.get_processes_or_404(process_name, [node_name])[0]
        node = self.get_node_or_404(node_name)
        try:
            if node.generate_connection().supervisor.stopProcess(process.name):
                return True, ""
            else:
                return False, "cannot stop process"
        except xmlrpc.client.Fault as err:
            return False, err.faultString
        except Exception as err:
            return False, str(err)

    def restart_process(self, process_name, node_name):
        process = self.get_processes_or_404(process_name, [node_name])[0]
        if process.state == 20:
            status, msg = self.stop_process(process_name, node_name)
            if not status:
                return status, msg

        return self.start_process(process_name, node_name)

    def serialize_general_node(self, _node):
        return {
            "Id": _node.id,
            "Name": _node.name,
            "Host": _node.host,
            "Port": _node.port,
            "Username": _node.username,
            "Password": _node.password,
            "State": XmlRpc.is_connected(self.connections.get(_node.name)),
        }

    def serialize_general_type(self, _type):
        rest = dict()
        rest['Type'] = _type
        for _p in self.processes:
            rest[_p.statename] = rest.get(_p.statename, 0) + 1

        return rest

    def serialize_general_environment(self, _environment):
        rest = dict()
        rest['Environment'] = _environment
        for _p in self.processes:
            rest[_p.statename] = rest.get(_p.statename, 0) + 1

        return rest
