# -*- encoding:utf-8 -*-

import salt.client


def salt_run(tgt, cmd, arg=()):
     local = salt.client.LocalClient()
     ret = local.cmd(tgt, cmd, arg)
     return ret

def restart_job_vir_salt(projects):
     with open("tomcat-quanfangzhen.txt") as f:
          lines = f.readlines()
     local = salt.client.LocalClient()
     jids = []
     for project in projects:
          target = ""
          for line in lines:
               if project == line.split()[0]:
                    target = line.split()[1]
                    # jid = local.cmd_async(target, 'cmd.run', ['/opt/deploy.sh %s'%project])
                    jid = local.cmd_async(target, 'cmd.run', ['/opt/deploy.sh %s'%project])
          jids.append(jid)
     return jids
'''

def run():
     def salt_run(tgt, cmd, arg=()):
          local = salt.client.LocalClient()
          ret = local.cmd(tgt, cmd, arg)
          return ret
     return salt_run
     
import salt.client
local = salt.client.LocalClient()
t = 0
jid = local.cmd_async('*', 'cmd.run', ['uptime'])
while not local.get_cache_returns(jid):
    time.sleep(1)
    if t == 8:
        print 'Connection Failed!'
        break
    else:
        t+=1
print local.get_cache_returns(jid)
'''
