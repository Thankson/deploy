# -*- encoding:utf-8 -*-

import jenkins

'''
jenkins_server_url = 'http://192.168.0.72/jenkins'
user_id = 'zqw'
api_token = '35351f256e54e74f43f6d89471a3036b'
# server=jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)
# job_name = '_Emulate_Restart_Project_test'
# param_dict = {"Boolean":"true", "ProjectName":"athena_back,tnt_order"}

# server.build_job(job_name, parameters=param_dict)
'''

def restart_job_vir_jenkins(projects):
    jenkins_server_url = 'http://192.168.0.72/jenkins'
    user_id = 'zqw'
    api_token = '35351f256e54e74f43f6d89471a3036b'
    server = jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)
    job_name = '_Emulate_Restart_Project_test'
    param_dict = {"Boolean": "true", "ProjectName": projects}
    server.build_job(job_name, parameters=param_dict)
    return job_name
