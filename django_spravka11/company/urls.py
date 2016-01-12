from django.conf.urls import patterns, url
from django.views.generic import ListView
from company import views

urlpatterns = patterns('',
    #url(r'^$', views.IndexView.as_view(), name='events_list'),
    #url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='events_detail'),
    url(r'^abc/$', views.CategoryABCList.as_view(), name='categoryabclist'),
    url(r'^abc/([\d-]+)/$', views.CategoryABCList.as_view(), name='categoryabclist'),
    url(r'^category/([\d-]+)/$', views.CompanyList.as_view(), name='companylist'),
    url(r'^news/$', views.CompanyNewsAll.as_view(), name='company_news'),
    url(r'^(?P<pk>\d+)/$', views.CompanyDetail.as_view(), name='company_detail'),
    url(r'^(?P<company_pk>\d+)/news/$', views.CurrentCompanyNewsAll.as_view(), name='current_company_news_all'),
    url(r'^(?P<company_pk>\d+)/news/(?P<news_pk>\d+)/$', views.CompanyNewsDetail.as_view(), name='current_company_news_detail'),
    url(r'^(?P<company_pk>\d+)/service/$', views.CurrentCompanyService.as_view(), name='current_company_service_all'),
    url(r'^(?P<company_pk>\d+)/service/(?P<service_pk>\d+)/$', views.CompanyServiceDetail.as_view(), name='current_company_service_detail'),
    url(r'^(?P<company_pk>\d+)/photo/$', views.CompanyImageAll.as_view(), name='current_company_photo'),
    url(r'^(?P<company_pk>\d+)/page/(?P<slug>\w+)/$', views.CompanyPageView.as_view(), name='current_company_page'),
    url(r'^search/$', views.CompanySearch.as_view(), name='search'),
    url(r'^form_company_error/', views.formcompanyerror),
    url(r'^form_company_backcall/', views.formcompanybackcall),
    url(r'^add_company/', views.addcompany, name='add_company'),
    url(r'^add_thanks/', views.addcompany),
    url(r'^search/autocomplete/', views.autocomplete),
)