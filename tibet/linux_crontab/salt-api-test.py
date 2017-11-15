#import salt.client
#
#local = salt.client.LocalClient()
#a = local.cmd('col', 'cmd.run', ['uptime'])
## local.cmd('*', 'test.fib', [10])
#print a

import salt.runner
import json, datetime

now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
opts = salt.config.master_config('/etc/salt/master')
runner = salt.runner.RunnerClient(opts)
b = runner.cmd('manage.status')
#print b
#print b['up']

b['now_time'] = now_time

with open('server_status.json', 'w') as f:
    json.dump(b, f)
    print 'load finish ...'
