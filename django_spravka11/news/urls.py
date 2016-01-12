from django.conf.urls import patterns, url
from django.views.generic import ListView
from news import views

urlpatterns = patterns('',
    #Возможно переделать вывод с использовнием вьюхи?
    #сделать проверку на первую страницу = главная
    url(r'^$', views.IndexView.as_view(), name='news_list'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='news_detail'),
    url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/$', views.CategoryListView.as_view(), name='news_category'),
    )