#!/usr/bin/env python
#decoding:utf-8
"""
	prepare.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.

configuration before you run flask
"""
from flask import Flask,g,request,render_template,jsonify,session
from google.appengine.api import users

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

from models import Tag,Link,SPost,User
import views,settings

MODULES=((views.frontend, ""),
    (views.post, "/post"),
    #(views.comment, "/comment"),
    (views.link, "/link"),
    (views.feeds, "/feeds"),
    (views.admin,'/admin'),
	(views.tag,'/tag'),
	(views.media,'/media'),
	(views.search,'/search')
)

def createapp():
	app=Flask('leepress')
	app.config.from_object(settings)
	configure_before_handlers(app)
	configure_errorhandlers(app)
	configure_modules(app)
	return app

def configure_before_handlers(app):

	@app.before_request
	def authenticate():
		#if g.user and g.user.email()!=settings.BLOGUSERMAIL:
		#	g.login=settings.NONE_LOGIN_TAG
		g.announceid=User.POST_ID
		g.tag=Tag.CachedTag
		g.link=Link.LinkListShow
		g.announcement=User.ANNOUNCEMENT

def configure_errorhandlers(app):

	@app.errorhandler(401)
	def unauthorized(error):
		if request.is_xhr:
			return jsonfiy(error="Login required")
		flash(_("Please login to see this page"), "error")
		return redirect(url_for("account.login", next=request.path))

	@app.errorhandler(403)
	def forbidden(error):
		if request.is_xhr:
			return jsonify(error='Sorry, page not allowed')
		return render_template("error/403.html", error=error)

	@app.errorhandler(404)
	def page_not_found(error):
		if request.is_xhr:
			return jsonify(error='Sorry, page not found')
		return render_template("error/404.html", error=error)

	@app.errorhandler(500)
	def server_error(error):
		if request.is_xhr:
			return jsonify(error='Sorry, an error has occurred')
		return render_template("error/500.html", error=error)


def configure_modules(app):
	for item in MODULES:
		app.register_blueprint(item[0],url_prefix=item[1])

