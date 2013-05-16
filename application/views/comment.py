#!/usr/bin/env python
#coding:utf-8
"""
	comment.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""

from flask import Blueprint,render_template,g,request,session
from application.models import SPost,Tag,User,Link,Media,Comment
from application.decorators import admin_required,login_required
import json,time,logging,urllib
from application.decorators import cached

comment=Blueprint('/comment',__name__,template_folder="../templates")

#@login_required
@comment.route('/newcomment/<int:post_id>',methods=['POST'])
def leavecomment(post_id=0):
	if 'user' not in session:
		status=0
		message="please login first"
	elif post_id==0:
		status=0
		message="comment to the wrong page"
	elif SPost.all().filter('post_id',post_id).get().allowcomment==False:
		status=0
		message="comment is not allowded here"
	else:
		logging.info('xxxxxxxxxxxxxxxx')
		logging.info(request.remote_addr)
		comment=Comment(post_id=post_id,
					email=session['user'].email(),
					nickname=session['user'].nickname(),
					comment=urllib.unquote(request.data).decode('utf-8'),
					create_date=int(time.time()),
					ip=request.remote_addr
					)
		comment.comment_id=Comment.properid()
		comment.put()
		status=1
		message=""
	Comment.updatecache()
	return json.dumps({"status":status,"message":message})


@comment.route('/get/<int:post_id>')
@cached(time=30*60)
def getcomment(post_id=0):
	comments=Comment.all().filter('post_id',post_id).order('-create_date').fetch(1000)
	comments=[i.getjsonobj() for i in comments]
	#logging.info(comments)
	return json.dumps(comments)

@comment.route('/delete',methods=['POST'])
@admin_required
def deletecomment():
	form=request.form
	commentlist=[]
	for item in form:
		commentlist.append(int(item))
	for item in commentlist:
		comment=Comment.all().filter('comment_id',item).get()
		if comment:
			comment.delete()
	Comment.updatecache()
	return json.dumps({'status':1})
