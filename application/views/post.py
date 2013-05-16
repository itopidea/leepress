#!/usr/bin/env python
#coding:utf-8
"""
	views: post.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""

import time
import mimetypes
import os,logging
import json as json
import urllib
from werkzeug.datastructures import Headers
from google.appengine.ext import blobstore
from flask import Blueprint, Response, request, flash, jsonify, g, current_app, \
	abort, redirect, url_for, session,send_file,render_template

from application.decorators import admin_required
from application.extensions import db
from application.models import User, SPost,Tag,Comment
from application.decorators import cached

post = Blueprint('post',__name__,template_folder="../templates")

@post.route("/<int:post_id>", methods=("GET","POST"))
@cached(time=60*60)
def getfullpost(post_id):
	post=SPost.all().filter('post_id',post_id).get()
	if post:
		comments=Comment.all().filter('post_id',post_id).order('-create_date').fetch(1000)
		return render_template('page.html',post=post,comments=comments)
	else:
		abort(404)
	# return render_template()

@post.route("/newpost",methods=['POST'])
@admin_required
def newpost():
	form=request.args
	newpost=SPost(title=form['title'],
				content=urllib.unquote(request.data).decode('utf-8'),
				num_lookup=0
				)
	if form['posttype']=='saveonly':
		newpost.saveonly=True
	else :
		newpost.saveonly=False
	if form.has_key('allowcomment') and form['allowcomment']=='on':
		newpost.allowcomment=True
	else :
		newpost.allowcomment=False
	newpost.post_id=SPost.properid()
	newpost.settags(form['tags'])
	newpost.create_date=int(time.time())
	newpost.update_time=newpost.create_date
	newpost.put()
	Tag.updatecache()
	SPost.updatecache()
	#return json.dumps({'message':newpost.content,'post_id':newpost.post_id})
	return json.dumps({'message':'success','post_id':newpost.post_id})

@post.route("/updatepost",methods=['POST'])
@admin_required
def updatepost():
	form =request.args
#	print request.data
	if form.has_key('post_id'):
		post=SPost.getone(form['post_id'])
		post.title=form['title']
		post.content=urllib.unquote(request.data).decode('utf-8')
		post.settags(form['tags'])
		post.update_time=int(time.time())
		if form['posttype']=='saveonly':
			post.saveonly=True
		else :
			post.saveonly=False
		if form.has_key('allowcomment') and form['allowcomment']=='on':
			post.allowcomment=True
		else :
			post.allowcomment=False
		post.put()
		Tag.updatecache()
		return json.dumps({'message':'success','post_id':form['post_id']})
	return "no such key exsits"

@post.route('/get/<int:post_id>')
@cached(time=60*60)
def getpost(post_id):
	'''
	if there is no such post return post_id=-1 
	'''
	post=SPost.all().filter('post_id',post_id).get()
	if post and post.saveonly==False:
		return post.getjson()
	else:
		return json.dumps({'post_id':-1})


@post.route('/delete',methods=['POST'])
@admin_required
def deletepage():
	form=request.form
	pagelist=[]
	for item in form:
		pagelist.append(int(item))
	for item in pagelist:
		post=SPost.all().filter('post_id',item).get()
		if post:
			post.remove()
	Tag.updatecache()
	SPost.updatecache()
	return json.dumps({'status':1})

#@post.route('/uploadimage',methods=['POST'])
#@admin_required
#def uploadimage():
#	form=request.form
#	img=request.files['mediaFile']
#	name=form['mediaName']
#	image=Image()
#	mimetype=img.content_type
#	imagename=image.save(img,name,mimetype)
#	return json.dumps({'serverImagePath':'/post/image/'+imagename})
#
#@post.route('/image/<filename>')
#def getimage(filename=None):
#	img=Image.all().filter('name',filename).get()
#	if not img:
#		abort(404)
#	else :
#		data=img.blob
#		mimetype =str( mimetypes.guess_type(img.name))
#		#fp=open('/home/fzlee/Desktop/a','w')
#		#fp.write(mimetype)
#		#fp.write(img.mimetype)
#		#fp.close()
#		return Response(data, mimetype=img.mimetype)
