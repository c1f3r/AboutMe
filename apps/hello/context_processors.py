from django.conf import settings


def settings_context_processor(request):
    return {u'settings': settings}