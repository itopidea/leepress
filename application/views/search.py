#!/usr/bin/env python
#coding:utf-8
"""
	search.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""
from flask import Blueprint,render_template,g,request
from application.models import SPost,Tag,User,Link,Media
from application.decorators import admin_required
from application.decorators import cached
import json


search=Blueprint('search',__name__,template_folder="../templates")


@search.route('')
@search.route('/')
@search.route('/<int:page>')
def dosearch(page=1):
	'''
	you can use 'and' operation here ,like a && b 
	'or' operation is not supported since it's of no use for me
	'''
	if 'search' not in request.args:
		return render_template('search.html',searchtag="",pagecount=0)
	searchtag=request.args['search']

	allpost=SPost.all().search(searchtag,['content'])

	pagecount=allpost.count()/User.SHOW_TAGSEARCH_NUMBER+1
	if allpost.count()%User.SHOW_TAGSEARCH_NUMBER==0:
		pagecount=pagecount-1
	return render_template('search.html',
							allpost=allpost,
							searchtag=searchtag,
							pagecount=pagecount)
