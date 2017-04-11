#!/usr/bin/python
import os
import sys

from flup.server.fcgi import WSGIServer
from django.core.wsgi import get_wsgi_application

sys.path.insert(0, "/home/w-sail/RITSailing")
os.environ['DJANGO_SETTINGS_MODULE'] = "RITSailing.settings"

WSGIServer(get_wsgi_application()).run()
