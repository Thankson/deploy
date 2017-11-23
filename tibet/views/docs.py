# -*- encoding:utf-8 -*-

from django.shortcuts import render

def manual(request):
    return render(request, 'docs/manual.html', locals())

def redis4singleinstall(request):
    return render(request, 'docs/redis-4_0_2-single_install.md.html', locals())