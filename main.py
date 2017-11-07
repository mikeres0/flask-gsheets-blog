from flask import Flask, render_template, Response, request, flash, url_for
import requests, json, random, os
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
from blog import Blog
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
app.secret_key = "dfoadhfoiawert834trjwernhfgp9werytawj"
cache = SimpleCache()

@app.route('/')
def index():
	gc = pygsheets.authorize(service_file='client_secret.json', no_cache=True)
	wks = gc.open("BlogDB").sheet1
	blogs = cache.get('blogs')
	data = []
	cached = ''

	if blogs is None:
		cached = 'false'
		rows = wks.get_all_records('', 1)
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
		cache.set('blogs', data, timeout= 5 * 60)
	else:
		cached = 'true'
		data = blogs

	return render_template('index.html', blogs=data, cached=cached)

if __name__ == "__main__":
	app.run()