""" A blog using Google Sheets as a DB, served as a Flask application """
from flask import Flask, render_template, redirect
from blog import Blog, GetBlogs
from werkzeug.contrib.cache import SimpleCache

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
        rows = GetBlogs()
        for i in rows:
            data.append(
                Blog(
                    blogid = i['BlogID'],
                    datecreated = i['DateCreated'],
                    title = i['Title'],
                    description = i['Description'],
                    content = i['Content'],
                    contenttype = i['ContentType'],
                    author = i['Author'],
                    tags = i['Tags']
                )
            )
        CACHE.set('blogs', data, timeout= 5 * 10)
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
