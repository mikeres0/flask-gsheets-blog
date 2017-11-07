""" file for interacting with blog objects """
import pygsheets


def get_blogs():
    """ return rows object containing blogs """
    _gc = pygsheets.authorize(service_file='client_secret.json', no_cache=True)
    _wks = _gc.open("BlogDB").sheet1
    _rows = _wks.get_all_records('', 1)
    return _rows


class Blog(object):  # pylint: disable=too-few-public-methods
    """ class object for blog """
    blogid = -1
    datecreated = ""
    title = ""
    description = ""
    content = ""
    contenttype = ""
    author = ""
    tags = ""

    def __init__(self):
        self = self
