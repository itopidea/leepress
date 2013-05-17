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
from application.models import User, SPost, Tag
from application.decorators import cached
from google.appengine.api import users
from application import settings 
import urllib

frontend = Blueprint('frontend',__name__,template_folder="../templates")

@frontend.route('/')
@frontend.route("/<int:page>")
def index(page=1):
	postlist=SPost.cached_get(False,User.PER_PAGE_IN_HOME,page);
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
	return redirect(users.create_login_url('/'))

@frontend.route('/logout')
def logout():
	return redirect(users.create_logout_url('/'))

@frontend.route('/loggedin')
def loggedin():
	#session.permanent=True
	#session['user']=users.get_current_user()
	#if session['user'].email()==settings.BLOGUSERMAIL:
	#	session['topbar']=settings.ADMIN_TAG
	#	session['admintoolbar']=settings.ADMIN_TOOL_BAR
	#else:
	#	session['topbar']=(('Welcome,'+session['user'].nickname(),"/logout"),)
	#return redirect('/')
	pass
