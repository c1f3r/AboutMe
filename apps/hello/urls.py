from django.conf.urls import patterns, url

from views import ViewInfoAboutMe, HttpRequestList


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', ViewInfoAboutMe.as_view(), name='index'),
    url(r'^requests/$', HttpRequestList.as_view(), name='requests'),
)
