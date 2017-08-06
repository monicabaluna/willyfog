from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^device_list/$', views.device_list, name='device_list'),
    url(r'^device/(?P<pk>\d+)/$', views.device_detail, name='device_detail'),
    url(r'^device/new/$', views.device_new, name='device_new'),
    url(r'^device/(?P<pk>\d+)/edit/$', views.device_edit, name='device_edit'),
    url(r'^device/(?P<pk>\d+)/remove/$', views.device_remove, name='device_remove'),
    url(r'^event/(?P<pk>\d+)/remove/$', views.event_remove, name='event_remove'),
    url(r'^device/(?P<pk>\d+)/command/$', views.add_command_to_device, name='add_command_to_device'),
    url(r'^device/(?P<pk>\d+)/schedule/$', views.schedule_command, name='schedule_command'),
    url(r'^device/(?P<pk>\d+)/trigger/$', views.trigger_command, name='trigger_command'),
    url(r'^device/(?P<device_pk>\d+)/trigger_one_command/(?P<command_pk>\d+)/$', views.trigger_one_command, name='trigger_one_command'),
]
