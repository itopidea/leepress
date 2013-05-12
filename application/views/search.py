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
import json


search=Blueprint('search',__name__,template_folder="../templates")


@search.route('/')
@search.route('/<searchtag>')
def dosearch(searchtag=None):
	'''
	you can use 'and' operation here ,like a && b 
	'or' operation is not supported since it's of no use for me
	'''
	if searchtag==None:
		return render_template('search.html',searchtag="",pagecount=0)

	searchlist=[]
	if '&&' in searchtag:
		searchlist=searchtag.split('&&')
		searchlist=[i.strip() for i in searchlist]
	else:
		searchlist=[searchtag]

	allpost=SPost.all()
	for eachsearch in searchlist:
		if eachsearch is not None:
			allpost=allpost.search(eachsearch,['content'])

	pagecount=allpost.count()/User.SHOW_TAGSEARCH_NUMBER+1
	if allpost.count()%User.SHOW_TAGSEARCH_NUMBER==0:
		pagecount=pagecount-1
	return render_template('search.html',
							allpost=allpost,
							searchtag=searchtag,
							pagecount=pagecount)
