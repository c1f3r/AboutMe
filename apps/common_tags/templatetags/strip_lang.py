from django import template
from django.utils.translation import get_language
import re

register = template.Library()

@register.filter
def strip_lang(path):
    pattern = '^(/%s)/' % get_language()
    match = re.search(pattern, path)
    if match is None:
        return path
    return path[match.end(1):]