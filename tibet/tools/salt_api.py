# -*- encoding:utf-8 -*-

import requests

def get_token():
    url = 'http://192.168.56.10:8000/login'
    login_data = {'username': 'test', 'password': 'test', 'eauth': 'pam'}
    headers = {'Accept': 'application/json'}
    res = requests.post(url, headers=headers, data=login_data)
    token = res.json()['return'][0]['token']
    return token

def saltCmd(ip, fun, *args, **kwargs):
    token = get_token()
    url = "http://192.168.56.10:8000"
    headers = {'Accept': 'application/json', "X-Auth-Token": token}
    res = requests.post(url, headers=headers, json= \
        {'client': 'local', 'tgt': ip, 'fun': fun, 'arg': list(args), 'kwarg': kwargs})
    response = res.json()['return']
    return response