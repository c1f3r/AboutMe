from django.contrib import admin

admin.autodiscover()

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns('',
                            url(r'^admin/', include(admin.site.urls)),
                            url(r'^accounts/login/$',
                                'django.contrib.auth.views.login',
                                name='login'),
                            url(r'^accounts/logout/$',
                                'django.contrib.auth.views.logout',
                                name='logout'),
                            url(r'^', include('apps.hello.urls')),
                            )

urlpatterns += patterns('', (r'^i18n/', include('django.conf.urls.i18n')),)
