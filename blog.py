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
            blog.authorsite = i['AuthorSite']
            blog.tags = i['Tags']
            data.append(blog)
        CACHE.set('blogs', data)
        return data
    return blogs

def get_blogs_with_category_id(categoryid):
    """ return rows object containing blogs for a specific category """
    cached_blogs = CACHE.get('category-' + str(categoryid))
    if cached_blogs is None:
        blogs = get_blogs()
        categorymatrix = CACHE.get('categorymatrix')
        data = []
        if categorymatrix is None:
            _gc = pygsheets.authorize(service_file='client_secret.json', no_cache=True)
            _wks = _gc.open("BlogDB").worksheet_by_title("CategoryMatrix")
            _rows = _wks.get_all_records('', 1)
            for i in filter(lambda x: x['CategoryID'] == categoryid, _rows):
                data.append(next(filter(lambda x: x.blogid == i['BlogID'], blogs)))
        CACHE.set('category-' + str(categoryid), data)
        return data
    return cached_blogs


def get_blog(url):
    """ return rows object containing blogs """
    blogs = CACHE.get('blogs')
    if blogs is None:
        data = get_blogs()
        blog = next(filter(lambda x: x.url == url, data))
        return blog
    blog = next(filter(lambda x: x.url == url, blogs))
    return blog

def get_categories():
    """ return rows object containing categories """
    categories = CACHE.get('categories')
    data = []
    if categories is None:
        _gc = pygsheets.authorize(service_file='client_secret.json', no_cache=True)
        _wks = _gc.open("BlogDB").worksheet_by_title("Categories")
        _rows = _wks.get_all_records('', 1)
        for i in _rows:
            category = Category()
            category.categoryid = i['CategoryID']
            category.title = i['Title']
            category.url = i['URL']
            data.append(category)
        CACHE.set('categories', data)
        return data
    return categories

def get_category(url):
    """ return rows object containing a category """
    categories = CACHE.get('categories')
    if categories is None:
        data = get_categories()
        category = next(filter(lambda x: x.url == url, data))
        return category
    category = next(filter(lambda x: x.url == url, categories))
    return category

def clear_cache():
    """ clears cache objects """
    CACHE.set('blogs', None, 1)
    CACHE.set('categories', None, 1)
    CACHE.set('categorymatrix', None, 1)


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

class Category(object):  # pylint: disable=too-few-public-methods
    """ class object for category """
    categoryid = -1
    title = ""
    url = ""

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
