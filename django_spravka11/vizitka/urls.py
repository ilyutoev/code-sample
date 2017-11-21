from django.conf.urls import patterns, url
from vizitka import views

urlpatterns = patterns('',
    url(r'^$', views.SubCompanyDetail.as_view(), name='sub_company_page'),
    url(r'^news/$', views.SubCurrentCompanyNewsAll.as_view(), name='sub_current_company_news_all'),
    url(r'^news/(?P<news_pk>\d+)/$', views.SubCompanyNewsDetail.as_view(), name='sub_current_company_news_detail'),
    url(r'^photo/$', views.SubCompanyImageAll.as_view(), name='sub_current_company_photo'),
    url(r'^service/$', views.SubCurrentCompanyService.as_view(), name='sub_current_company_service_all'),
    url(r'^service/(?P<service_pk>\d+)/$', views.SubCompanyServiceDetail.as_view(), name='sub_current_company_service_detail'),
    url(r'^page/(?P<slug>\w+)/$', views.SubCompanyPageView.as_view(), name='sub_current_company_page'),
)