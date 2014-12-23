from apps.hello.models import HttpRequestLog


class HttpRequestLogMiddleware(object):
    """
    middleware which saves each HttpRequest to DB
    """

    def process_request(self, request):
        request_log = HttpRequestLog()
        request_log.host = request.get_host()
        request_log.path = request.get_full_path()
        request_log.method = request.method
        if request.user.is_authenticated():
            request_log.user = request.user
        request_log.save()
