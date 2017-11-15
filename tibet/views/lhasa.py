# -*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from tibet.tools.salt_api import saltCmd
#from tibet.tools.jenkins_api import restart_job_vir_jenkins
from tibet.tools.salt_api_client import restart_job_vir_salt
from tibet.tools.utils import clean_data, single_list

from tibet.models import RestartJobs

import datetime

def index(request):
    return render(request, 'lhasa/index.html', locals())

def commond(request):
    return render(request, 'lhasa/commond.html', locals())

def commondexe(request):
    target = request.GET['target']
    fun = request.GET['modules']
    args = request.GET['args']
    kwargs = request.GET['kwargs']
    res = saltCmd(target, fun, args, kwargs)
    return HttpResponse(res)

def restart_fz(request):
    applicant = '小明'
    pro = 'vst_back'
    get_all_restart = RestartJobs.objects.get_all_restart_by_time()
    print get_all_restart
    return render(request, 'lhasa/restart_fz.html', locals())

def machine_status(request):
    return render(request, 'lhasa/machine_status.html', locals())

def restart_fz_shenqing(request):
    pro_name = request.POST.get('project', '')
    pro_name2 = request.POST.getlist('pro', '')
    print pro_name
    print type(pro_name)
    print pro_name2
    print type(pro_name2)
    pro_name = clean_data(pro_name)
    projects = pro_name + pro_name2
    print projects
    projects = single_list(projects)
    projects = ','.join(projects)
    note = request.POST.getlist('note', '')
    try:
        new_job = RestartJobs(projects=projects, note=note)
        new_job.save()
    except:
        raise
    return HttpResponse(projects)

def restart_fz_r(request):

    resid = None
    time = datetime.datetime.now()
    if request.method == 'GET':
        resid = request.GET['resid']
        if resid:
            lt = RestartJobs.objects.get(id=int(resid))
            projects = lt.projects
            projects_list = projects.split(",")
            jids = restart_job_vir_salt(projects_list)
            #jobname = restart_job_vir_jenkins(projects)
            #cus = RestartJobs.objects.filter(id=int(resid)).update(restarttime=time, jenksins_job_name=jobname)
            #lt2 = RestartJobs.objects.get(id=int(resid))
            #restarttime = lt2.restarttime.strftime("%Y-%m-%d %H:%M:%S")
            return HttpResponse(jids)

def testt(request):
    return render(request, 'lhasa/testt2.html', locals())

