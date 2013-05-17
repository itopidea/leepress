#!/usr/bin/env python
#coding:utf-8
"""
	extensions.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.

"""
#from flask import Flask,g,request,render_template
from google.appengine.api import users

#import sys 
#reload(sys) 
#sys.setdefaultencoding('utf8')

#import settings
#from models import Tag,Link,Post,User
# from google.appengine.ext import ndb as db
from google.appengine.ext import db
from google.appengine.api import search 
Index=search.Index(name="Post")

#__all__ = ['mail', 'cache', 'photos']

