# -*- encoding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect


from tibet.tools.salt_api import saltCmd
#from tibet.tools.jenkins_api import restart_job_vir_jenkins
from tibet.tools.salt_api_client import restart_job_vir_salt
from tibet.tools.utils import clean_data, single_list
from tibet.tools.salt_http_api_async import SaltApi, salt_api

from tibet.models import RestartJobs, MiddwearDeploy, HostList, HostServiceStatus

import datetime, json, time

from django.contrib.auth.decorators import permission_required,login_required




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
    user = request.user
    applicant = '小明'
    pro = 'vst_back'
    get_all_restart = RestartJobs.objects.get_all_restart_by_time()
    print get_all_restart
    return render(request, 'lhasa/restart_fz.html', locals())

#@login_required
def mac(request):
    user = request.user
    all_hosts = HostList.objects.all()
    return render(request, 'lhasa/mac.html', locals())

@permission_required('tibet.add_hostlist', login_url='/')
def mac_add(request):
    if request.method == 'GET':
        name = request.GET['name']
        ip = request.GET['ip']
        restart_cmd = request.GET['recmd']
        service = request.GET['ser']
        note = request.GET['note'] or ''
        try:
            macadd = HostList(ip=ip,hostname=name,service=service,restart_cmd=restart_cmd,note=note)
            macadd.save()
        except Exception as e:
            return HttpResponse('fail')
        else:
            return HttpResponse('ok')

@permission_required('tibet.delete_hostlist', login_url='/')
def mac_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        HostList.objects.filter(id=id).delete()
        return HttpResponseRedirect('/mac')

@permission_required('tibet.change_hostlist', login_url='/')
def mac_edit(request,id=None):
    # user = request.user 这一句很关键，要不然html文件中找不到头像和用户的基本信息了
    user = request.user
    if request.method == 'GET':
        id = request.GET.get('id')
    #all_idc = Idc.objects.all()
    all_host=HostList.objects.filter(id=id)
    return render_to_response("lhasa/mac_edit.html",locals())

def macresult(request):
    if request.method =='GET':
        id2 = request.GET.get('id')
        name = request.GET['name']
        ip = request.GET['ip']
        restart_cmd = request.GET['recmd']
        service = request.GET['ser']
        note = request.GET['note'] or ''
        a = int(id2)
        try:
            HostList.objects.filter(id=a).update(ip=ip,hostname=name,service=service,restart_cmd=restart_cmd,note=note)
        except Exception as e:
            print e
            print "get exception"
            return HttpResponse('fail')
        else:
            return HttpResponse('ok')

        # finally:
        #     return HttpResponse('ok')

def mac_status_refresh(request):
    try:
        target = HostList.objects.values_list('hostname','service')
    except Exception as e:
        print e
        print "get exception"
        return HttpResponse('fail')

    salt_client = ','.join([a[0] for a in target])
    #target =
    try:
        salt1 = SaltApi(salt_api)
    except Exception as e:
        print e
        inf = 'ret code 4'
        print 'ret code 4'
        return HttpResponse(inf)

    salt_method = 'cmd.run'
    # project = 'tntnt222'
    # salt_params = '/opt/deploy.sh %s' % project
    salt_params = 'bash /opt/chk_service_status.sh'
    try:
        result = salt1.salt_command_list(salt_client, salt_method, salt_params)
        # print "result"
        # print result
        # print 'resultend'
        # result1 = salt1.look_jid(jid1)
        # for i in result1.keys():
        #     print i
        #     print result1[i]
    except Exception as e:
        print e
        inf = 'ret code 3'
        print 'ret code 3'
        return HttpResponse(inf)
    for tar in target:
        # print tar[1]
        # print tar[0]
        if tar[0] in result:
            if not result[tar[0]]:
                HostList.objects.filter(hostname=tar[0]).update(status_tmp='down')
                HostServiceStatus.objects.create(status='down')
                continue
            if tar[1] in result[tar[0]]:
                HostList.objects.filter(hostname=tar[0]).filter(service=tar[1]).update(status_tmp='on')
            else:
                HostList.objects.filter(hostname=tar[0]).filter(service=tar[1]).update(status_tmp='down')
        else:
            HostList.objects.filter(hostname=tar[0]).update(status_tmp='notAMinion')

    status = HostList.objects.values_list('id', 'status_tmp')
    print status[0][1]
    ret = list(status)
    ret2 = json.dumps(ret)
    print ret2
    return HttpResponse(ret2)

def restart_fz_shenqing(request):
    user = request.user
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
        new_job = RestartJobs(applicant=user, projects=projects, note=note)
        new_job.save()
    except:
        raise
    return HttpResponse(projects)

def restart_fz_r(request):
    user = request.user
    username = user.username
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
                            # result1 = salt1.look_jid(jid1)
                            # for i in result1.keys():
                            #     print i
                            #     print result1[i]
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
            cus = RestartJobs.objects.filter(id=int(resid)).update(restarttime=time, operator=username)
            #lt2 = RestartJobs.objects.get(id=int(resid))
            #restarttime = lt2.restarttime.strftime("%Y-%m-%d %H:%M:%S")
            return HttpResponse(restarted_job)
        else:
            return HttpResponse('restart failed!')

#@permission_required('tibet.change_group', login_url='/login/')
@permission_required('crashstats.can_view_url', login_url='/')
def get_midd_deploy(request):
    return render(request, 'lhasa/midd_deploy.html', locals())


def post_midd_deploy(request):
    # pro_name2 = request.POST.getlist('pro', '')
    user = request.user
    # print user
    # print 'a'
    # #print request.user.groups.name
    # print user.perms.crashstats.can_view_url
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

def testt2(request):
    return render(request, 'lhasa/testt2.html', locals())

def testt3(request):
    return render(request, 'lhasa/testt3.html', locals())

def testt33(request):
    time.sleep(1)
    print '111222'
    return HttpResponse('inf')