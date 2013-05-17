#!/usr/bin/env python
#coding:utf-8
"""
	task.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""
from flask import Blueprint,render_template,g,request
from application.models import SPost,Tag,User,Link,Media,Comment
from application.decorators import admin_required
import json,logging

from google.appengine.api import memcache
task=Blueprint('task',__name__,template_folder="../templates")

from google.appengine.ext import deferred
from google.appengine.ext import db

@task.route('/dotask')
@admin_required
def dotask():
	one=User.all().get()
	one.delete()
	return "update successfully"



