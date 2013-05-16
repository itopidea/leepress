#!/usr/bin/env python
#coding:utf-8
"""
	frontend.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""

import datetime,logging
import os,json
from flask import Blueprint, Response, request, flash, jsonify, g, current_app,\
	abort, redirect, url_for, session, send_file, send_from_directory, render_template 
from application.extensions import db
from application.models import User, SPost, Tag,Post
from application.decorators import cached
from google.appengine.api import users
from application import settings 
import urllib

frontend = Blueprint('frontend',__name__,template_folder="../templates")

#@frontend.route('/test/<sch>')
#def hello123(sch):
#	result=SPost.all().search(sch,['content'])
#	body=""
#	for item in result:
#		logging.info(item.content)
#		body=body+item.content
#
#	return str(body)
#
#@frontend.route('/dotasks')
#def dotasks():
#	allpost=Post.all().fetch(1000,0)
#	for one in allpost:
#		newpost=SPost(title=one.title,
#					content=one.content,
#					create_date=one.create_date,
#					update_time=one.update_time,
#					tags=one.tags,
#					saveonly=one.saveonly,
#					allowcomment=one.allowcomment,
#					num_lookup=one.num_lookup,
#					post_id=one.post_id)
#		newpost.put()
#	return "yes"

@frontend.route('/')
@frontend.route("/<int:page>")
@cached(time=30*60)
def index(page=1):
	postlist=SPost.get(False,User.PER_PAGE_IN_HOME,page);
	pagecount=SPost.PostCount/User.PER_PAGE_IN_HOME+1

	if SPost.PostCount%User.PER_PAGE_IN_HOME==0:
		pagecount=pagecount-1
	currentpage=page

	if postlist or page==1:
		return render_template("index.html",
							postlist=postlist,
							currentpage=currentpage,
							pagecount=pagecount)
	else :
		return render_template("error/index_not_found.html")
	
@frontend.route('/login')
def selflogin():
	return redirect(users.create_login_url('/loggedin'))

@frontend.route('/logout')
def logout():
	session.pop('user')
	return redirect('/')

@frontend.route('/loggedin')
def loggedin():
	session.permanent=True
	session['user']=users.get_current_user()
	if session['user'].email()==settings.BLOGUSERMAIL:
		session['topbar']=settings.ADMIN_TAG
		session['admintoolbar']=settings.ADMIN_TOOL_BAR
	else:
		session['topbar']=(('Welcome,'+session['user'].nickname(),"/logout"),)
	return redirect('/')
