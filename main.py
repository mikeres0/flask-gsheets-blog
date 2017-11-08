""" A blog using Google Sheets as a DB, served as a Flask application """
from flask import Flask, render_template, redirect
from blog import Blog, get_blogs
from werkzeug.contrib.cache import SimpleCache
import markdown2

APP = Flask(__name__)
APP.secret_key = "dfoadhfoiawert834trjwernhfgp9werytawj"
CACHE = SimpleCache()


@APP.route('/')
def index():
    """ the index view or blog list page """
    blogs = CACHE.get('blogs')
    data = []
    cached = ''

    if blogs is None:
        cached = 'false'
        rows = get_blogs()
        for i in rows:
            blog = Blog()
            blog.blogid = i['BlogID']
            blog.datecreated = i['DateCreated']
            blog.title = i['Title']
            blog.description = i['Description']
            blog.content = i['Content']
            blog.contenttype = i['ContentType']
            blog.author = i['Author']
            blog.authorsite = i['AuthorSite']
            blog.tags = i['Tags']
            if blog.contenttype == 'MARKDOWN':
                blog.content = markdown2.markdown(blog.content)
            data.append(blog)
        CACHE.set('blogs', data, timeout=5*60)
    else:
        cached = 'true'
        data = blogs

    return render_template('index.html', blogs=data, cached=cached)


@APP.route('/clear-cache')
def clearcache():
    """ clears blogs cache object """
    CACHE.set('blogs', None, timeout=1)
    return redirect('/')

if __name__ == "__main__":
    APP.run()
