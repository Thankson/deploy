#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import requests
import json
try:
    import cookielib
except:
    import http.cookiejar as cookielib

# 使用urllib2请求https出错，做的设置
import ssl
context = ssl._create_unverified_context()

# 使用requests请求https出现警告，做的设置
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


salt_api = "http://192.168.2.197:8000/"


class SaltApi:
    """
    定义salt api接口的类
    初始化获得token
    """
    def __init__(self, url):
        self.url = url
        self.username = "test"
        self.password = "test"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
            # "Content-type": "application/x-yaml"
        }
        self.params = {'client': 'local', 'fun': '', 'tgt': ''}
        # self.params = {'client': 'local', 'fun': '', 'tgt': '', 'arg': ''}
        self.login_url = salt_api + "login"
        self.login_params = {'username': self.username, 'password': self.password, 'eauth': 'pam'}
        self.token = self.get_data(self.login_url, self.login_params)['token']
        self.headers['X-Auth-Token'] = self.token

    def get_data(self, url, params):
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        # response = request.text
        # response = eval(response)     使用x-yaml格式时使用这个命令把回应的内容转换成字典
        # print response
        # print request
        # print type(request)
        response = request.json()
        result = dict(response)
        # print result
        return result['return'][0]

    def salt_command(self, tgt, method, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        if arg:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt}
        print '命令参数: ', params
        result = self.get_data(self.url, params)
        return result


    def salt_async_command(self, tgt, method, arg=None):  # 异步执行salt命令，根据jid查看执行结果
        """远程异步执行命令"""
        if arg:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt}
        jid = self.get_data(self.url, params)['jid']
        return jid

    def look_jid(self, jid):  # 根据异步执行命令返回的jid查看事件结果
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        print params
        result = self.get_data(self.url, params)
        return result



'''
def main():
    print '=================='
    print '同步执行命令'
    salt = SaltApi(salt_api)
    print salt.token
    salt_client = '*'
    salt_test = 'test.ping'
    salt_method = 'cmd.run'
    salt_params = 'free -m'
    # print salt.salt_command(salt_client, salt_method, salt_params)
    # 下面只是为了打印结果好看点
    result1 = salt.salt_command(salt_client, salt_test)
    for i in result1.keys():
        print i, ': ', result1[i]
    result2 = salt.salt_command(salt_client, salt_method, salt_params)
    for i in result2.keys():
        print i
        print result2[i]
        print

if __name__ == '__main__':
    main()
'''