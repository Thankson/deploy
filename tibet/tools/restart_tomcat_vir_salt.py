# -*- encoding:utf-8 -*-

from salt_http_api_async import SaltApi, salt_api

import os, sys, time, re
import fileinput
import requests
from multiprocessing import Pool

def server_start(ip, project, arg=()):
    try:
        salt1 = SaltApi(salt_api)
    except Exception as e:
        print e
        inf = 'ret code 2'
        print 'ret code 2'
    salt_client = ip
    salt_method = 'cmd.run'
    salt_params = '/opt/deploy.sh %s' % project
    try:
        jid1 = salt1.salt_async_command(salt_client, salt_method, salt_params)
        time.sleep(8)
    except Exception as e:
        print e
        inf = 'ret code 3'
        print 'ret code 3'


def url_check(ip, project, arg=()):
    # url = 'http://%s:%s/%s/checkversion.jsp'%(ip, 'port', project)
    url = 'http://%s:%s/%s/checkversion.jsp' % ('192.168.0.172', '8080', 'super_back')
    try:
        r = requests.get(url)
        r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        if r.status_code == 200:
            ret = True
        else:
            ret = False
    except requests.RequestException as e:
        print e
        ret = False
    return ret


def start_queue(project):
    ips = []
    pattern = "^%s$"%project
    print project
    for line in fileinput.input('tomcat-quanfangzhen.txt', inplace=False, mode='r'):
        if re.search(pattern, line.split()[0]):
            ip = line.split()[1]
            ips.append(ip)
    print "Begin to start %s ..."%project
    print ips
    for ip in ips:
        print ip
        server_start(ip, project)
        start = time.time()
        while not url_check(ip, project):
            time.sleep(2)
            print 'waiting...'
            end = time.time()
            if (end - start) > (20):
                print "time out"
                break

def start(alljobs):
    p = Pool()
    for i in alljobs:
        p.apply_async(start_queue, args=(i,))
    print 'Start starting all chosed project...'
    p.close()
    p.join()
    print 'All projects started.'