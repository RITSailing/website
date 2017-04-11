from django.http import HttpResponseRedirect
from .responseutils import HttpRedirectException
from django.core.urlresolvers import reverse
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

class HttpRedirect(object):
    def process_exception(self, request, exception, *args, **kwargs):
        if isinstance(exception, HttpRedirectException):
            url = reverse(exception.args[0])
            array = exception.args[1]
            keys = list(array.keys())
            items = list(array.items())
            values = [items[keys.index("email")], items[keys.index("first_name")], items[keys.index("last_name")]]
            params = urlencode(values, True)
            return HttpResponseRedirect(url + "?%s" % params)
