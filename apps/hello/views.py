from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from models import AboutUser, HttpRequestLog


# Create your views here.


class ViewInfoAboutMe(DetailView):
    """CBV for viewing info about me"""

    model = AboutUser

    def get_object(self, queryset=None):
        return AboutUser.objects.get(username=u"cifer")

    template_name = u'hello/index.html'
    context_object_name = u'about_me'


class HttpRequestList(ListView):
    template_name = u'hello/requests.html'
    context_object_name = u'requests'

    def get_queryset(self):
        return HttpRequestLog.objects.order_by('-date_time')[:10]