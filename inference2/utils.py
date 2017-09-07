# -*- coding: utf-8 -*-

import json
from contextlib import closing

import unicodecsv


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def json_to_csv(jsonData, fieldnames=None):
    """
    Returns a CSV string from the given JSON data string.
    """
    d = json.loads(jsonData)
    fieldnames = fieldnames or d[0].keys()
    return dict_to_csv(d, fieldnames)


def dict_to_csv(d, fieldnames):
    """
    Returns a CSV string from the given list of dictionaries.
    """
    buf = None
    with closing(StringIO.StringIO()) as f:
        dictWriter = unicodecsv.DictWriter(f, fieldnames)
        dictWriter.writeheader()
        dictWriter.writerows(d)

        buf = f.getvalue()

    return buf
