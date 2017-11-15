import re

def clean_data(mess_job):
    job_name = re.split('\s|,|\n', mess_job)
    job_name = [x for x in job_name if x]
    return job_name

def single_list(ids):
    func = lambda x, y: x if y in x else x + [y]
    res = reduce(func, [[], ] + ids)
    return res