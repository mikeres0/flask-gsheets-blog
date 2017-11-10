""" A blog using Google Sheets as a DB, served as a Flask application """
from flask import Flask, render_template, redirect
from werkzeug.contrib.cache import SimpleCache
import blog
import markdown2

APP = Flask(__name__)
APP.secret_key = "dfoadhfoiawert834trjwernhfgp9werytawj"
CACHE = SimpleCache()


@APP.route('/')
def index():
    """ the index view or blog list page """
    return render_template('home/index.html', blogs=blog.get_blogs())


@APP.route('/clear-cache')
def clearcache():
    """ clears blogs cache object """
    blog.clear_cache()
    return redirect('/')

if __name__ == "__main__":
    APP.run()
