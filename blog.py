""" file for interacting with blog objects """
import pygsheets
from werkzeug.contrib.cache import SimpleCache
CACHE = SimpleCache()

def get_blogs():
    """ return rows object containing blogs """
    blogs = CACHE.get('blogs')
    data = []
    if blogs is None:
        _gc = pygsheets.authorize(service_file='client_secret.json', no_cache=True)
        _wks = _gc.open("BlogDB").worksheet_by_title("Home")
        _rows = _wks.get_all_records('', 1)
        for i in _rows:
            blog = Blog()
            blog.blogid = i['BlogID']
            blog.url = i['URL']
            blog.datecreated = i['DateCreated']
            blog.title = i['Title']
            blog.description = i['Description']
            blog.content = i['Content']
            blog.contenttype = i['ContentType']
            blog.author = i['Author']
            blog.tags = i['Tags']
            data.append(blog)
        CACHE.set('blogs', data, timeout=5*60)
        return data
    else:
        return blogs


def get_blog(url):
    """ return rows object containing blogs """
    blogs = CACHE.get('blogs')
    if blogs is None:
        data = get_blogs()
        blog = next(filter(lambda x: x.url == url, data))
        return blog
    else:
        blog = next(filter(lambda x: x.url == url, blogs))
        return blog


def clear_cache():
    """ clears cache objects """
    CACHE.set('blogs', None, 1)


class Blog(object):  # pylint: disable=too-few-public-methods
    """ class object for blog """
    blogid = -1
    datecreated = ""
    url = ""
    title = ""
    description = ""
    content = ""
    contenttype = ""
    author = ""
    authorsite = ""
    tags = ""

    def __init__(self):
        self = self

class Breadcrumb(object):  # pylint: disable=too-few-public-methods
    """ class object for breadcrumbs """
    url = ""
    title = ""

    def __init__(self, url, title):
        self.title = title
        self.url = url
        self = self