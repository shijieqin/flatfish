import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from core.flatfish import Flatfish
from .models import Node

# Create your views here.
from django.views.decorators.http import require_http_methods


@login_required(login_url='/myauth/login')
def home(request):
    user = request.user
    return render(request, 'supervisor/home.html', locals())


@login_required(login_url='/myauth/login')
def node(request):
    return render(request, 'supervisor/node.html', locals())


@login_required(login_url='/myauth/login')
@require_http_methods(["POST"])
def node_query(request):
    _instance = Flatfish.getInstance(request.user)
    data = request.POST
    returnData = {"rows": []}
    for _node in _instance.nodes:
        serialize_node = _instance.serialize_general_node(_node)
        serialize_node.pop('Username')
        serialize_node.pop('Password')
        returnData['rows'].append(serialize_node)
    return JsonResponse(returnData)


@login_required(login_url='/myauth/login')
def node_detail(request, node_name):
    _instance = Flatfish.getInstance(request.user)
    print(node_name)
    return render(request, 'supervisor/node_detail.html', locals())


@login_required(login_url='/myauth/login')
def node_detail_query(request, node_name):
    _instance = Flatfish.getInstance(request.user)
    data = request.POST
    returnData = {"rows": []}
    for _process in _instance.processes_tree.get(node_name):
        returnData["rows"].append({
            "NodeName": node_name,
            "Name": _process.name,
            "Pid": _process.pid,
            "Group": _process.group,
            "Type": _process.type,
            "Environment": _process.environment,
            "Uptime": _process.uptime,
            "State": _process.statename,
            "StateCode": _process.state
        })
    return JsonResponse(returnData)


@login_required(login_url='/myauth/login')
def process_stop(request):
    _instance = Flatfish.getInstance(request.user)
    result = {"msg": "success", "code": 0, "error_num": 0, "success_num": 0}
    error_num = 0
    success_num = 0
    data = request.POST
    processes = json.loads(data['processes'])
    print(processes)
    for process in processes:
        node_name = process[0]
        process_name = process[1]
        if _instance.stop_process(process_name=process_name, node_name=node_name):
            success_num += 1
        else:
            error_num += 1
    if error_num > 0:
        result["code"] = 1
        result["msg"] = "some process stop failed"
    if success_num == 0:
        result["code"] = -1
        result["msg"] = "all process stop failed"

    return JsonResponse(result)


@login_required(login_url='/myauth/login')
def process_start(request):
    _instance = Flatfish.getInstance(request.user)
    result = {"msg": "success", "code": 0, "error_num": 0, "success_num": 0}
    error_num = 0
    success_num = 0
    data = request.POST
    processes = json.loads(data['processes'])
    print(processes)
    for process in processes:
        print(process)
        node_name = process[0]
        process_name = process[1]
        if _instance.start_process(process_name=process_name, node_name=node_name):
            success_num += 1
        else:
            error_num += 1
    if error_num > 0:
        result["code"] = 1
        result["msg"] = "some process start failed"
    if success_num == 0:
        result["code"] = -1
        result["msg"] = "all process start failed"

    return JsonResponse(result)


@login_required(login_url='/myauth/login')
def process_restart(request):
    _instance = Flatfish.getInstance(request.user)
    result = {"msg": "success", "code": 0, "error_num": 0, "success_num": 0}
    error_num = 0
    success_num = 0
    data = request.POST
    processes = json.loads(data['processes'])
    print(processes)
    for process in processes:
        node_name = process[0]
        process_name = process[1]
        if _instance.restart_process(process_name=process_name, node_name=node_name):
            success_num += 1
        else:
            error_num += 1
    if error_num > 0:
        result["code"] = 1
        result["msg"] = "some process restart failed"
    if success_num == 0:
        result["code"] = -1
        result["msg"] = "all process restart failed"

    return JsonResponse(result)


@login_required(login_url='/myauth/login')
def read_process_log(request):
    if request.method == "POST":
        _instance = Flatfish.getInstance(request.user)
        logs = ''
        result = {"msg": "success", "code": 0, "logs": logs}
        data = request.POST
        process = json.loads(data['process'])
        node_name = process[0]
        process_name = process[1]
        logs = _instance.get_process_logs(process_name, node_name)
        result = {"msg": "success", "code": 0, "logs": logs}
        return JsonResponse(result)


@login_required(login_url='/myauth/login')
@require_http_methods(["POST"])
def add_node(request):
    if not request.user.is_superuser:
        return JsonResponse({"msg": "没有权限", "code": -1})
    _instance = Flatfish.getInstance(request.user)
    print('test add_node')
    result = {"msg": "success", "code": 0}
    name = request.POST['name']
    host = request.POST['host']
    port = request.POST['port']
    username = request.POST['username']
    password = request.POST['password']

    same_name_node = Node.objects.filter(name=name)
    if same_name_node:
        result = {"msg": "node name 已存在", "code": 1}
        return JsonResponse(result)

    same_name_host_port = Node.objects.filter(Q(host=host) & Q(port=port))
    if same_name_host_port:
        result = {"msg": "node 已存在", "code": 1}
        return JsonResponse(result)

    _node = Node()
    _node.name = name
    _node.host = host
    _node.port = port
    _node.username = username
    _node.password = password
    _node.save()
    _instance.reload()
    return JsonResponse(result)


@login_required(login_url='/myauth/login')
def type(request):
    return render(request, 'supervisor/type.html', locals())


@login_required(login_url='/myauth/login')
@require_http_methods(["POST"])
def type_query(request):
    _instance = Flatfish.getInstance(request.user)
    data = request.POST
    returnData = {"rows": []}
    for _type in _instance.types:
        returnData['rows'].append(_instance.serialize_general_type(_type))
    return JsonResponse(returnData)


@login_required(login_url='/myauth/login')
def type_detail(request, type_name):
    _instance = Flatfish.getInstance(request.user)
    print(type_name)
    return render(request, 'supervisor/type_detail.html', locals())


@login_required(login_url='/myauth/login')
def type_detail_query(request, type_name):
    _instance = Flatfish.getInstance(request.user)
    data = request.POST
    returnData = {"rows": []}
    for _process in _instance.get_processes_by_type_name(type_name):
        returnData["rows"].append({
            "NodeName": _process.node,
            "Name": _process.name,
            "Pid": _process.pid,
            "Group": _process.group,
            "Type": _process.type,
            "Environment": _process.environment,
            "Uptime": _process.uptime,
            "State": _process.statename,
            "StateCode": _process.state
        })
    return JsonResponse(returnData)


@login_required(login_url='/myauth/login')
def environment(request):
    return render(request, 'supervisor/environment.html', locals())


@login_required(login_url='/myauth/login')
@require_http_methods(["POST"])
def environment_query(request):
    _instance = Flatfish.getInstance(request.user)
    data = request.POST
    returnData = {"rows": []}
    for _environment in _instance.environments:
        returnData['rows'].append(_instance.serialize_general_environment(_environment))
    return JsonResponse(returnData)


@login_required(login_url='/myauth/login')
def environment_detail(request, environment_name):
    _instance = Flatfish.getInstance(request.user)
    print(environment_name)
    return render(request, 'supervisor/environment_detail.html', locals())


@login_required(login_url='/myauth/login')
def environment_detail_query(request, environment_name):
    _instance = Flatfish.getInstance(request.user)
    data = request.POST
    returnData = {"rows": []}
    for _process in _instance.get_processes_by_environment_name(environment_name):
        returnData["rows"].append({
            "NodeName": _process.node,
            "Name": _process.name,
            "Pid": _process.pid,
            "Group": _process.group,
            "Type": _process.type,
            "Environment": _process.environment,
            "Uptime": _process.uptime,
            "State": _process.statename,
            "StateCode": _process.state
        })
    return JsonResponse(returnData)


@login_required(login_url='/myauth/login')
def process(request):
    return None