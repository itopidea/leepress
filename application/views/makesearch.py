#!/usr/bin/env python
#coding:utf-8
"""
	search.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""
from flask import Blueprint,render_template,g,request
from application.models import Post,Tag,User,Link,Media
from application.decorators import admin_required
from application.decorators import cached
from application.extensions import Index
from google.appengine.api import search 
import json


makesearch=Blueprint('search',__name__,template_folder="../templates")



#@search.route('')
#@search.route('/')
#@search.route('/<int:page>')
#def dosearch(page=1):
#	if 'search' not in request.args:
#		return render_template('search.html',searchtag="",pagecount=0)
#	searchtag=request.args['search']
#
#	allpost=Post.all().search(searchtag,['content'])
#
#	pagecount=allpost.count()/User.SHOW_TAGSEARCH_NUMBER+1
#	if allpost.count()%User.SHOW_TAGSEARCH_NUMBER==0:
#		pagecount=pagecount-1
#	return render_template('search.html',
#							allpost=allpost,
#							searchtag=searchtag,
#							pagecount=pagecount)


@makesearch.route('')
@makesearch.route('/')
@makesearch.route('/<int:page>')
def dosearch(page=1):
	if 'search' not in request.args:
		return render_template('search.html',searchtag="",pagecount=0)
	searchtag=request.args['search']
	query_options=search.QueryOptions(
		sort_options=search.SortOptions(
			expressions=[search.SortExpression(expression='title',default_value="")],
			),
		ids_only=True
		)
	query_obj=search.Query(query_string=searchtag,options=query_options)
	allpost=Index.search(query=query_obj)
	allpostid=[int(i.doc_id) for i in allpost.results]

	allpost=Post.cached_get_by_id_list(allpostid)
	#allpost=Post.all().filter('post_id in',allpostid)

	pagecount=allpost.count()/User.SHOW_TAGSEARCH_NUMBER+1
	if allpost.count()%User.SHOW_TAGSEARCH_NUMBER==0:
		pagecount=pagecount-1
	return render_template('search.html',
							allpost=allpost,
							searchtag=searchtag,
							pagecount=pagecount)

