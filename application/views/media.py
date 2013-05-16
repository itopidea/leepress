#!/usr/bin/env python
#coding:utf-8
"""
	media.py
	~~~~~~~~~~~~~
"""

from flask import Blueprint,render_template,g,request,Response
from application.models import SPost,Tag,User,Link,Media
from application.decorators import admin_required
from application.settings import BLOGUSERMAIL
from application.decorators import cached
import json
import mimetypes
import time,logging

media=Blueprint('media',__name__,template_folder="../templates")

@media.route('/upload',methods=['POST'])
@admin_required
def uploadmedia():
	form=request.form
	fp=request.files['mediaFile']
	name=form['mediaName']
	display=True
	#if not form.has_key('display'):
	#	display=False
	blob=fp.read()
	size=len(blob)
	nowtime=int(time.time())
	media=Media(name=name,size=size,create_date=nowtime,display=display)
	media.putcontent(blob)
	media.put()
	Media.updatecache()
	return json.dumps({'serverImagePath':'/media/get/'+str(media.blobkey)+'/'+media.name})

@media.route('/get/<media_id>/<fpname>')
@cached(time=24*60*60)
def getmedia(media_id,fpname):
	media=Media.getmediainfo(media_id)
	if not media or media.name!=fpname:
		abort(404)
	elif media.display==False and g.user.email()!=BLOGUSERMAIL:
		abort(404)
	else :
		data=Media.getmedia(media_id)
		mimetype=mimetypes.guess_type(media.name)
		mimetype=mimetype[0] if len(mimetype)>0 else ""
		return Response(data,mimetype=mimetype)

@media.route('/delete',methods=['POST'])
@admin_required
def remove():
	form=request.form
	removelist=[]
	for item in form:
		removelist.append(item)
	Media.deletelist(removelist)
	Media.updatecache()
	return json.dumps({'message':'success'})

@media.route('/update',methods=['POST'])
@admin_required
def update():
	form=request.form
	display=True
	updatelist=[]
	for item in form:
		if form[item]=='checked':
			display=True
		else:
			display=False
	updatelist.append((item,display))
	Media.updatemedia(updatelist)
	Media.updatecache()
	return json.dumps({'message':'success'})




