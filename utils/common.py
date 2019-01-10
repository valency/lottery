import json
import xml.etree.ElementTree

import requests

SUPPORT_PLATFORMS = (
    ('5C', 'http://www.500.com/'),
    ('HK-CH', 'http://www.hkjc.com/'),
    ('HK-EN', 'http://www.hkjc.com/'),
    ('MS', 'http://www.macauslot.com/'),
    ('BF', 'http://www.betfair.com/')
)


def load_url(url, encoding='UTF-8'):
    response = requests.Session().get(url).content
    if encoding is not None:
        response = response.decode(encoding)
    return response


def load_json(url, encoding=None):
    return json.loads(load_url(url, encoding))


def load_xml(url, encoding=None):
    return xml.etree.ElementTree.fromstring(load_url(url, encoding))


def dict_search(dictionary, key, value):
    for i in range(0, len(dictionary)):
        if dictionary[i][key] == value:
            return i
    return None


def string_insert(str1, str2, i):
    return str1[:i] + str2 + str1[i:]
