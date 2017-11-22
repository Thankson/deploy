# -*- encoding:utf-8 -*-

from django.shortcuts import render

def manual(request):
    return render(request, 'docs/manual.html', locals())