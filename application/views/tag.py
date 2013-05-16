#!/usr/bin/env python
#coding:utf-8
"""
	views: post.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, Response, request, flash, jsonify, g, current_app,\
	abort, redirect, url_for, session, send_file, send_from_directory,render_template

from application.models import Tag,SPost,User
import urllib

tag = Blueprint('tag',__name__,template_folder="../templates")

@tag.route('')
@tag.route('/')
@tag.route('/<int:page>')
def searchtagname(page=1):
	if 'tagname' not in request.args:
		return render_template('tag.html',allposst=[],pagecount=0,currentpage=1,tagname="")
	tagname=urllib.unquote(request.args['tagname']).decode('utf-8')

	allpost=SPost.all().filter('saveonly',False)
	tagnamelist=tagname.split(',')
	for eachtag in tagnamelist:
		eachtag=eachtag.strip()
		allpost.filter('tags',eachtag)
	#.filter('tags',tagname)
	pagecount=allpost.count()/User.SHOW_TAGSEARCH_NUMBER+1
	if allpost.count()%User.SHOW_TAGSEARCH_NUMBER==0:
		pagecount=pagecount-1
	allpost=allpost.fetch(User.SHOW_TAGSEARCH_NUMBER,(page-1)*User.SHOW_TAGSEARCH_NUMBER)
	if allpost:
		return render_template('tag.html',allpost=allpost,pagecount=pagecount,currentpage=page,tagname=tagname)
	else:
		return render_template('error/tag_not_found.html',tagname=tagname)
