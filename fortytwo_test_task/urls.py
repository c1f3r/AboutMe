from django.contrib import admin

admin.autodiscover()

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings

urlpatterns = i18n_patterns('',
                            # Examples:
                            # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
                            # url(r'^blog/', include('blog.urls')),

                            url(r'^admin/', include(admin.site.urls)),
                            url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
                            url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
                            url(r'^', include('apps.hello.urls')),
)

urlpatterns += patterns('',
                        (r'^i18n/', include('django.conf.urls.i18n')),
)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )