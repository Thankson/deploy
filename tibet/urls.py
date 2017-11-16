from django.conf.urls import url
from views import common, lhasa, result, user

urlpatterns = [
    url(r'^login/$', common.method_splitter, {'GET': user.get_login, 'POST': user.post_login}, name='login'),
    url(r'^register/$', common.method_splitter, {'GET': user.get_register, 'POST': user.post_register}, name='register'),
    url(r'^logout/$', common.method_splitter, {'GET': user.get_logout}, name='logout'),
    url(r'^forgot/$', common.method_splitter, {'GET': user.get_forgotpwd, 'POST': user.post_forgotpwd}, name='forgot'),
    url(r'^members/$', common.method_splitter, {'GET': user.get_members}, name='members'),
    url(r'^setting/$', common.method_splitter, {'GET': user.get_setting, 'POST': user.post_setting}, name='setting'),
    url(r'^setting/password/$', common.method_splitter, {'GET': user.get_settingpwd, 'POST': user.post_settingpwd}, name='set_passwd'),
    url(r'^setting/avatar/$', common.method_splitter, {'GET': user.get_setting_avatar, 'POST': user.post_setting_avatar}, name='set_ava'),
    url(r'^u/(.*)/$', common.method_splitter, {'GET': user.get_profile}),

    url(r'^$', common.method_splitter, {'GET': lhasa.index}, name='index'),
    url(r'^commond/$', common.method_splitter, {'GET': lhasa.commond}, name='commond'),
    url(r'^commondexe$', lhasa.commondexe),
    url(r'^restart_fz$', common.method_splitter, {'GET': lhasa.restart_fz}, name='restart_fz'),
    url(r'^restart_fz_shenqing$', lhasa.restart_fz_shenqing),
    url(r'^restart_fz/restart$', lhasa.restart_fz_r),
    url(r'^machine_status$', common.method_splitter, {'GET': lhasa.machine_status}, name='machine_status'),

    url(r'^midd-deploy/$', common.method_splitter, {'GET': lhasa.get_midd_deploy, 'POST': lhasa.post_midd_deploy}, name='midd-deploy'),

    url(r'^testt$', lhasa.testt),

    # json urls
    url(r'^serverstatus$', result.serverstatus),
    url(r'^projects$', result.projects),

    url(r'^pcstatus_test$', result.pcstatus_test),
    url(r'^serverstatus_test$', result.serverstatus_test),
]