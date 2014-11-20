from PIL import Image
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from forms import EditInfoForm

from models import AboutUser, HttpRequestLog




# Create your views here.


class ViewInfoAboutMe(DetailView):
    """CBV for viewing info about me"""

    template_name = u'hello/index.html'
    context_object_name = u'about_me'

    def get_object(self, queryset=None):
        return AboutUser.objects.get(username=u"cifer")



class HttpRequestList(ListView):
    template_name = u'hello/requests.html'
    context_object_name = u'requests'

    def get_queryset(self):
        return HttpRequestLog.objects.order_by('-date_time')[:10]


class EditInfoAboutMe(UpdateView):

    model = AboutUser
    form_class = EditInfoForm
    template_name = u'hello/edit_info.html'

    def get_object(self, queryset=None):
        return AboutUser.objects.get(username=u'cifer')

    def form_valid(self, form):
        form_object = form.save()
        if form_object.avatar:
            img = Image.open(form_object.avatar.path)
            img.thumbnail((200, 200), Image.ANTIALIAS)
            img.save(img.filename, "JPEG")
        return super(EditInfoAboutMe, self).form_valid(form)

