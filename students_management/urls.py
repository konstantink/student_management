import os 

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from app.views import *

site_media = os.path.join(os.path.dirname(__file__), 'site-media')
images = site_media+'/uploads/images'

urlpatterns = patterns('',
    # Examples:
    url(r'^$', main_page),
    url(r'^group/(\d+)', group_page),
    url(r'^group/edit', group_form_page),
    url(r'^group/save', group_form_page),
    url(r'^group/add', group_form_page),
    url(r'^student/(\d+)', student_page),
    url(r'^student/add', student_form_page),
    url(r'^site-media/(?P<path>.*)', 'django.views.static.serve', {'document_root' : site_media}),
    url(r'^student/photo/(?P<path>.*)', 'django.views.static.serve', {'document_root' : images}),
    # url(r'^students_management/', include('students_management.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
