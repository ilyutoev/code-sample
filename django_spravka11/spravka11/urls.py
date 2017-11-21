from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from company.views import site_index, admin_company_import_export
from misc.views import admin_afisha_import
from misc.views import count_form, contact_form
from filebrowser.sites import site

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/filebrowser/', include(site.urls)),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/company_import/', admin_company_import_export),
    url(r'^admin/afisha_import/', admin_afisha_import),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', site_index, name='index'),
    url(r'^news/',include('news.urls')),
    url(r'^events/',include('events.urls')),
    url(r'^company/',include('company.urls')),
    url(r'^banners/', include('banners.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^page/count/$', count_form, name='count_form'),
    url(r'^page/contact_thanks/$', contact_form, name='contact_form'),
    url(r'^page/', include('django.contrib.flatpages.urls')),
    url(r'^p/', include('vizitka.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),
        )

urlpatterns += patterns(
    url(r'^page/', include('django.contrib.flatpages.urls')),
    )