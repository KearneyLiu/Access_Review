from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^login$', 'access_review.views.my_login',  name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^manager_register$', 'access_review.views.manager_register',name='manager_register'),
    url(r'^auditor_register$', 'access_review.views.auditor_register',name='auditor_register'),
    url(r'^admin_register$', 'access_review.views.admin_register',name='admin_register'),

    url(r'^home$', 'access_review.views.home',name='home'),
    url(r'^audit$', 'access_review.views.audit', name='audit'),
    url(r'^admin$', 'access_review.views.admin', name='admin'),
    url(r'^$', 'access_review.views.welcome', name='welcome'),

    url(r'^add_data$', 'access_review.views.addData', name='add_data'),
    url(r'^add_data_2$', 'access_review.views.addData_2', name='add_data_2'),
    url(r'^add_data_3$', 'access_review.views.addData_3', name='add_data_3'),


    url(r'^permission/(?P<id>\d+)$', 'access_review.views.edit_permission', name='edit_permission'),
    url(r'^view_permission/(?P<id>\d+)$', 'access_review.views.view_permission', name='view_permission'),

    url(r'^view_assignment/(?P<id>\d+)$', 'access_review.views.view_assignment', name='view_assignment'),
    url(r'^assign_manager/(?P<id1>\d+)/(?P<id2>\d+)$', 'access_review.views.assign_manager', name='assign_manager'),
    url(r'^remove_manager/(?P<id1>\d+)/(?P<id2>\d+)$', 'access_review.views.remove_manager', name='remove_manager'),

    url(r'^assign_auditor/(?P<id1>\d+)/(?P<id2>\d+)$', 'access_review.views.assign_auditor', name='assign_auditor'),
    url(r'^remove_auditor/(?P<id1>\d+)/(?P<id2>\d+)$', 'access_review.views.remove_auditor', name='remove_auditor'),

    url(r'^upload_file/(?P<id>\d+)$', 'access_review.views.upload_file', name='upload_file'),
    url(r'^upload/(?P<id>\d+)$', 'access_review.views.upload', name='upload'),

    url(r'^audit_permission/(?P<id>\d+)$', 'access_review.views.audit_permission', name='audit_permission'),
    url(r'^report_pdf/(?P<id>\d+)$', 'access_review.views.report_pdf', name='report_pdf'),

)
