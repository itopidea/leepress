#!/usr/bin/env python
#coding:utf-8
"""
	admin.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""

from flask import Blueprint,render_template,g,request
from application.models import SPost,Tag,User,Link,Media
from application.decorators import admin_required
import json

adminor=Blueprint('admin',__name__,template_folder="../templates")

#@adminor.route("/")
#@admin_required
#def admin():
#	return render_template("admin/admin.html")

@adminor.route("/post",methods=['POST','GET'])
@adminor.route("/post/<int:post_id>",methods=['POST','GET'])
@admin_required
def post(post_id=None):
	post=None
	if post_id!=None:
		post=SPost.getone(post_id)
	return render_template('admin/post.html',post=post)

@adminor.route("/")
@adminor.route("/page")
@adminor.route('/page/<int:page>')
@admin_required
def page(page=1):
	postlist=SPost.get(True,User.PER_PAGE_IN_ADMIN,page)
	pagecount=SPost.AllCount/User.PER_PAGE_IN_ADMIN+1
	if SPost.AllCount%User.PER_PAGE_IN_ADMIN==0:
		pagecount=pagecount-1
	return render_template('admin/pagelist.html',
			postlist=postlist,
			currentpage=page,
			pagecount=pagecount)

@adminor.route('/link')
@admin_required
def link():
	alllink=Link.all().order('-link_id').fetch(100)
	return render_template('admin/link.html',link=alllink)


@adminor.route('/setting',methods=['GET','POST'])
@admin_required
def setting():
	if request.method=='GET':
		post_id=User.POST_ID
		postnumberhome=User.PER_PAGE_IN_HOME
		postnumberadmin=User.PER_PAGE_IN_ADMIN
		showtagnumber=User.SHOW_TAG_NUMBER
		showtagsearchnumber=User.SHOW_TAGSEARCH_NUMBER
		showlinknumber=User.SHOW_LINK_NUMBER
		mediainadmin=User.MEDIA_IN_ADMIN
		announcelength=User.ANNOUNCELENGTH
		return render_template('admin/setting.html',
							post_id=post_id,
							postnumberhome=postnumberhome,
							postnumberadmin=postnumberadmin,
							showtagnumber=showtagnumber,
							showtagsearchnumber=showtagsearchnumber,
							showlinknumber=showlinknumber,
							mediainadmin=mediainadmin,
							announcelength=announcelength
							)
	else :
		needupdate=False
		form=request.form
		one=User.all().get()
		one.postnumberhome=int(form['postnumberhome'])
		one.postnumberadmin=int(form['postnumberadmin'])
		one.showtagnumber=int(form['showtagnumber'])
		one.showmediaadmin=int(form['mediainadmin'])
		one.announcelength=int(form['announcelength'])
		if int(form['showtagsearchnumber'])!=one.showtagsearchnumber:
			needupdate=True
		one.showtagsearchnumber=int(form['showtagsearchnumber'])
		one.showlinknumber=int(form['showlinknumber'])
		one.post_id=int(form['post_id'])
		another=SPost.all().filter('post_id',int(form['post_id'])).get()
		if not another:
			one.post_id=-1
		
		one.put()
		User.updatecache(one)
		Tag.updatecache()

		return json.dumps({'message':'success'})


@adminor.route('/media',methods=['GET'])
@adminor.route('/media/<int:page>')
@admin_required
def media(page=1):
	medialist=Media.getall(True,User.MEDIA_IN_ADMIN,page)
	pagecount=Media.Allcount/User.MEDIA_IN_ADMIN+1
	if Media.Allcount%User.MEDIA_IN_ADMIN==0:
		pagecount=pagecount-1
	
	return render_template('admin/media.html',
							medialist=medialist,
							pagecount=pagecount,
							currentpage=page)
