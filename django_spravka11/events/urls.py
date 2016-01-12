from django.conf.urls import patterns, url
from django.views.generic import ListView
from events import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='events_list'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='events_detail'),
    url(r'^place/(?P<pk>\d+)/$', views.PlaceView.as_view(), name='events_place'),
    url(r'^rubr/(?P<rubr_pk>\d+)/$', views.IndexView.as_view(), name='eventtype_list'),
    url(r'^rubr/(?P<rubr_pk>\d+)/day/(?P<day>\d+)/$', views.IndexView.as_view(), name='eventtype_day_list'),
    url(r'^day/(?P<day>\d+)/$', views.IndexView.as_view(), name='days_list'),

#2 варианта - все по дате 
# - в рубрике по дате 
    )