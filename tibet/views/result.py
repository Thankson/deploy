# -*- encoding:utf-8 -*-

from django.shortcuts import render

def serverstatus(request):
    return render(request, 'result_json/server_status.json', locals())

def projects(request):
    return render(request, 'result_json/projects.json', locals())



def pcstatus_test(request):
    return render(request, 'result_json/userinfo_test.json', locals())

def serverstatus_test(request):
    return render(request, 'result_json/da_test.json', locals())