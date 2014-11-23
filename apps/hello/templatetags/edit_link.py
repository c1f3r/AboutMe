from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def edit_link(object_to_edit):
    object_to_edit_content_type = ContentType.objects.get_for_model(object_to_edit)
    # return object_to_edit_content_type.app_label, object_to_edit_content_type.model, object_to_edit.pk
    return reverse(u"admin:{0.app_label}_{0.model}_change".format(object_to_edit_content_type), args=(object_to_edit.id, ))