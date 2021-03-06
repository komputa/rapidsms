#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^$',
        'rapidsms.contrib.httptester.views.generate_identity',
        {'backend_name': 'message_tester'}, name='httptester-index'),
    url(r"^(?P<backend_name>[\w-]+)/$", views.generate_identity),
    url(r"^(?P<backend_name>[\w-]+)/(?P<identity>\d+)/$",
        views.message_tester,
        name='httptester')
)
