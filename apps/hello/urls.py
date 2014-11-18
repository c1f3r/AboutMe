from django.conf.urls import patterns, include, url
from views import ViewInfoAboutMe

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', ViewInfoAboutMe.as_view(), name='index')
)
