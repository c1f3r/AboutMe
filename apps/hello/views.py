import json

from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

import django_tables2 as tables

from apps.hello.forms import EditInfoForm
from apps.hello.models import AboutUser, HttpRequestLog


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
            return HttpResponse("OK")
        else:
            return response


class EditInfoAboutMe(AjaxableResponseMixin, UpdateView):
    model = AboutUser
    form_class = EditInfoForm
    template_name = u'hello/edit_info.html'
    success_url = reverse_lazy(u'edit_info')

    def get_object(self, queryset=None):
        return AboutUser.objects.get(username=u'cifer')
