#!/usr/bin/env python
#coding:utf-8
"""
	decorators.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.

Decorators for URL handlers
"""


from functools import wraps
from google.appengine.api import users
from flask import redirect, request, abort,g,session
from application.settings import BLOGUSERMAIL


def admin_required(func):
	"""Requires standard login credentials"""
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if 'user' in session and session['user'].email() ==  BLOGUSERMAIL:
			return func(*args, **kwargs)
		else :
			return redirect(users.create_login_url(request.url))
	return decorated_view

def login_required(func):
	@wraps(func)
	def decorated_view(*args,**kargs):
		if 'user' in session:
			return func(*args,**kargs)
		else :
			return redirect(users.create_login_url(request.url)) 
	return decorated_view
