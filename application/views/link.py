#!/usr/bin/env python
#coding:utf-8
"""
	views: link.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, Response, request, flash, jsonify, g, current_app,\
	abort, redirect, url_for, session,render_template
import json
import time
from application.extensions import db

from application.models import Link
from application.decorators import admin_required

link = Blueprint('link',__name__,template_folder="../templates")

@link.route("/")
def index():
	showlink=Link.LinkListShow		
	return render_template("link.html", showlink=showlink)

@link.route("/add",methods=['POST'])
@admin_required
def add():
	form=request.form
	newlink=Link(name=form['name'],
				link=form['link'],
				description=form['description'])
	if  form.has_key('display') and form['display']=='on':
		newlink.display=True
	else:
		newlink.display=False

	
	newlink.create_date=int(time.time())
	newlink.link_id=Link.properid()
	newlink.put()
	Link.updatecache()
	return json.dumps({'message':'success'})

@link.route("/delete",methods=['POST'])
@admin_required
def mydelete():
	form=request.form
	deletelist=[]
	for item in form:
		deletelist.append(int(item))
	Link.deletelist(deletelist)
	Link.updatecache()	
	return json.dumps({'message':'success'})


@link.route('/update',methods=['POST'])
@admin_required
def myupdate():
	form=request.form
	updatelist=[]
	display=True
	for item in form:
		if form[item]=='checked':
			display=True
		else :
			display=False
		updatelist.append((int(item),display))
	Link.updatelist(updatelist)
	Link.updatecache()
	return json.dumps({'message':'success'})





















