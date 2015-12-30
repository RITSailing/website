from django.http import HttpResponseRedirect
from responseutils import HttpRedirectException
from django.core.urlresolvers import reverse
import urllib

class HttpRedirect(object):
    def process_exception(self, request, exception, *args, **kwargs):
        if isinstance(exception, HttpRedirectException):
            url = reverse(exception.args[0])
            array = exception.args[1]
            values = [array.items()[array.keys().index("email")], array.items()[array.keys().index("first_name")], array.items()[array.keys().index("last_name")]]
            params = urllib.urlencode(values)
            return HttpResponseRedirect(url + "?%s" % params)
