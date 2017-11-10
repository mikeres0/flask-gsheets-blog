""" A blog using Google Sheets as a DB, served as a Flask application """
from flask import Flask, render_template, redirect
from werkzeug.contrib.cache import SimpleCache
import blog

APP = Flask(__name__)
APP.secret_key = "dfoadhfoiawert834trjwernhfgp9werytawj"
CACHE = SimpleCache()


@APP.route('/')
def index():
    """ the index view for blog list page """
    return render_template('home/index.html',
                           blogs=blog.get_blogs(),
                           categories=blog.get_categories(),
                           activenav='home')

@APP.route('/post/<url>')
def post_index(url):
    """ the index view for post page """
    post = blog.get_blog(url)
    breadcrumbs = []
    breadcrumbs.append(blog.Breadcrumb(title=post.title, url='/post/{0}'.format(post.url)))
    return render_template('post/index.html',
                           blog=post,
                           categories=blog.get_categories(),
                           breadcrumbs=breadcrumbs)

@APP.route('/category/<url>')
def category_index(url):
    """ the index view for post page """
    category = blog.get_category(url)
    blogs = blog.get_blogs_with_category_id(category.categoryid)
    breadcrumbs = []
    breadcrumbs.append(
        blog.Breadcrumb(
            title=category.title,
            url='/category/{0}'.format(category.url)
        )
    )
    return render_template('category/index.html',
                           blogs=blogs,
                           category=category,
                           categories=blog.get_categories(),
                           breadcrumbs=breadcrumbs,
                           activenav='category')


@APP.route('/clear-cache')
def clearcache():
    """ clears blogs cache object """
    blog.clear_cache()
    return redirect('/')

if __name__ == "__main__":
    APP.run()
