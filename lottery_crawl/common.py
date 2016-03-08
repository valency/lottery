import json
import urllib2
from datetime import datetime


def print_green(prt):
    return "\033[92m {}\033[00m".format(prt)


def log(msg):
    print print_green("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] ") + msg


def load_url(url, encoding=None):
    response = urllib2.urlopen(url).read()
    if encoding is not None:
        response = unicode(response, encoding).encode('UTF-8')
    return response


def load_json(url):
    return json.loads(load_url(url))
