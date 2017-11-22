# -*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from tibet.tools.salt_api import saltCmd
#from tibet.tools.jenkins_api import restart_job_vir_jenkins
from tibet.tools.salt_api_client import restart_job_vir_salt
from tibet.tools.utils import clean_data, single_list
from tibet.tools.salt_http_api_async import SaltApi, salt_api

from tibet.models import RestartJobs, MiddwearDeploy

import datetime

from django.contrib.auth.decorators import permission_required

######################################
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
#
#
#
# url_content_type = ContentType.objects.create(model='unused')
#
# can_view_url = Permission.objects.create(name='can view url', content_type=url_content_type,codename='can_view_url')


######################################


def index(request):
    return render(request, 'lhasa/index.html', locals())

#@permission_required('can_view_url', login_url='/login/')
def commond(request):
    return render(request, 'lhasa/commond.html', locals())

def commondexe(request):
    target = request.GET['target']
    fun = request.GET['modules']
    args = request.GET['args']
    kwargs = request.GET['kwargs']
    res = saltCmd(target, fun, args, kwargs)
    return HttpResponse(res)

#@permission_required('tibet.change_group', login_url='/login/')
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

            with open("tomcat-quanfangzhen.txt") as f:
                lines = f.readlines()
            jids = []
            restarted_job = []
            try:
                salt1 = SaltApi(salt_api)
            except Exception as e:
                print e
                inf = 'ret code 2'
                print 'ret code 2'
                return HttpResponse(inf)
            for project in projects_list:
                target = ""
                for line in lines:
                    if project == line.split()[0]:
                        target = line.split()[1]
                        # jid = local.cmd_async(target, 'cmd.run', ['/opt/deploy.sh %s'%project])
                        salt_client = target
                        salt_method = 'cmd.run'
                        salt_params = '/opt/deploy.sh %s' % project
                        try:
                            jid1 = salt1.salt_async_command(salt_client, salt_method, salt_params)
                        except Exception as e:
                            print e
                            inf = 'ret code 3'
                            print 'ret code 3'
                            return HttpResponse(inf)
                        #jid = local.cmd_async(target, 'cmd.run', ['/opt/deploy.sh %s' % project])
                        jids.append(jid1)
                        restarted_job.append('{%s => %s}'%(target, project))
            #jids = restart_job_vir_salt(projects_list)

            #jobname = restart_job_vir_jenkins(projects)
            #cus = RestartJobs.objects.filter(id=int(resid)).update(restarttime=time, jenksins_job_name=jobname)
            #lt2 = RestartJobs.objects.get(id=int(resid))
            #restarttime = lt2.restarttime.strftime("%Y-%m-%d %H:%M:%S")
            return HttpResponse(restarted_job)
        else:
            return HttpResponse('restart failed!')

#@permission_required('tibet.change_group', login_url='/login/')
def get_midd_deploy(request):
    return render(request, 'lhasa/midd_deploy.html', locals())


def post_midd_deploy(request):
    # pro_name2 = request.POST.getlist('pro', '')
    user = request.user
    print user
    print 'a'
    #print request.user.groups.name
    print user.has_perm('tibet.change_group')
    #group = groups.objects.all()
    minion_id = request.POST.get('minion_id', '')
    middware = request.POST.get('middware', '')
    edition = request.POST.get('edition', '')
    clustter = request.POST.get('clustter', '')
    note = request.POST.getlist('note', '')
    #salt_params = 'test.redis-4_0_2-single.install'
    #salt_params = ''
    if middware == 'redis':
        if edition == "redis4.0.2":
            if clustter == "single":
                salt_params = 'test.redis-4_0_2-single.install'
            else:
                pass
        else:
            pass
    elif middware == 'dubbo':
        pass
    elif middware == 'nginx':
        pass
    elif middware == 'mongodb':
        pass
    else:
        pass

    try:
        salt1 = SaltApi(salt_api)
        print salt_api
        salt_client = minion_id
        salt_method = 'state.sls'

        jid1 = salt1.salt_async_command(salt_client, salt_method, salt_params)
        print jid1
    except Exception as e:
        print e
        inf = 'ret code 1'
        print 'ret code 1'
        return HttpResponse(inf)
    #print jid1
    try:
        new_job = MiddwearDeploy(deployer=user, minion_id=minion_id, middware=middware, edition=edition, clustter=clustter, jid=jid1, note=note)
        new_job.save()
    except:
        raise
    inf = "deploy middware %s edition %s clustter %s on machine %s"%(middware, edition, clustter,minion_id)
    return HttpResponse(inf)



def testt(request):
    return render(request, 'lhasa/testt.html', locals())

