from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from apps.hello.views import ViewInfoAboutMe, HttpRequestList, EditInfoAboutMe


urlpatterns = patterns('',
                       url(r'^$', ViewInfoAboutMe.as_view(), name='index'),
                       url(r'^requests/$', HttpRequestList.as_view(),
                           name='requests'),
                       url(r'^edit_info/$',
                           login_required(EditInfoAboutMe.as_view()),
                           name='edit_info'),
                       )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
