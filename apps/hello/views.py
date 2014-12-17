import json
from django.views.generic import TemplateView
import django_tables2 as tables

from PIL import Image
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
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


class HttpRequestLogTable(tables.Table):
    class Meta:
        model = HttpRequestLog
        order_by = 'date_time'
        attrs = {'class': 'paleblue'}


class HttpRequestList(tables.SingleTableView):
    model = HttpRequestLog
    table_class = HttpRequestLogTable
    context_table_name = u'requests'
    table_pagination = {'per_page': 10}

    template_name = u'hello/requests.html'
    '''
class HttpRequestList(ListView):
    template_name = u'hello/requests.html'
    context_object_name = u'requests'

    def get_queryset(self):
        return HttpRequestLogTable(HttpRequestLog.objects.all())
'''

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,

            }
            return self.render_to_json_response(data)
        else:
            return response


class EditInfoAboutMe(AjaxableResponseMixin, UpdateView):
    model = AboutUser
    form_class = EditInfoForm
    template_name = u'hello/edit_info.html'
    success_url = reverse_lazy(u'edit_info')

    def get_object(self, queryset=None):
        return AboutUser.objects.get(username=u'cifer')

    def form_valid(self, form):
        form_object = form.save()
        if form_object.avatar:
            img = Image.open(form_object.avatar.path)
            img.thumbnail((200, 200), Image.ANTIALIAS)
            img.save(img.filename, "JPEG")
        return super(EditInfoAboutMe, self).form_valid(form)

