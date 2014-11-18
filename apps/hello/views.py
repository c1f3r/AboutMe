from django.views.generic.detail import DetailView
from models import AboutUser

# Create your views here.


class ViewInfoAboutMe(DetailView):
    """CBV for viewing info about me"""

    model = AboutUser

    def get_object(self, queryset=None):
        return AboutUser.objects.get(username=u"cifer")

    template_name = u'hello/index.html'
    context_object_name = u'about_me'