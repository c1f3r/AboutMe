from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def edit_link(object_to_edit):
    """
    Returns link to administration page for editing objects in DB
    :param object_to_edit:
    :return:
    """
    obj_to_edit_cont_type = ContentType.objects.get_for_model(object_to_edit)
    url_str = u"admin:{0.app_label}_{0.model}_change"
    return reverse(url_str.format(obj_to_edit_cont_type),
                   args=(object_to_edit.id, )
                   )
