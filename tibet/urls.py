from django.conf.urls import url
from views import common, lhasa, result

urlpatterns = [
    url(r'^$', common.method_splitter, {'GET': lhasa.index}, name='index'),
    url(r'^commond/$', common.method_splitter, {'GET': lhasa.commond}, name='commond'),
    url(r'^commondexe$', lhasa.commondexe),
    url(r'^restart_fz$', common.method_splitter, {'GET': lhasa.restart_fz}, name='restart_fz'),
    url(r'^restart_fz_shenqing$', lhasa.restart_fz_shenqing),
    url(r'^restart_fz/restart$', lhasa.restart_fz_r),
    url(r'^machine_status$', common.method_splitter, {'GET': lhasa.machine_status}, name='machine_status'),

    url(r'^testt$', lhasa.testt),

    # json urls
    url(r'^serverstatus$', result.serverstatus),
    url(r'^projects$', result.projects),

    url(r'^pcstatus_test$', result.pcstatus_test),
    url(r'^serverstatus_test$', result.serverstatus_test),
]