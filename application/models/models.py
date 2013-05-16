#!/usr/bin/env python
#coding:utf-8
"""
	models.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""
import json as json
from google.appengine.ext import blobstore
from application.extensions import db
from google.appengine.api import files
from application import settings
import becer,logging

from google.appengine.api import memcache

class User(db.Model):
	postnumberhome=db.IntegerProperty()
	postnumberadmin=db.IntegerProperty()
	showtagnumber=db.IntegerProperty()
	showtagsearchnumber=db.IntegerProperty()
	showlinknumber=db.IntegerProperty()
	showmediaadmin=db.IntegerProperty()
	commentinadmin=db.IntegerProperty()
	commentinsidebar=db.IntegerProperty()
	#use one post for announcement
	post_id=db.IntegerProperty()
	announcelength=db.IntegerProperty()

	#how many posts are shown in the home page
	PER_PAGE_IN_HOME=15
	PER_PAGE_IN_ADMIN=50
	#how many tags are shown in home page
	SHOW_TAG_NUMBER=20
	#how many tags are shown in tag search page 
	SHOW_TAGSEARCH_NUMBER=20
	SHOW_LINK_NUMBER=10
	COMMENT_IN_ADMIN=20
	COMMENT_IN_SIDEBAR=10
	MEDIA_IN_ADMIN=20

	ANNOUNCEMENT="xy"
	POST_ID=-1
	ANNOUNCELENGTH=100
	@classmethod
	def updatecache(cls,one=None):
		if not one:
			one=User.all().get()
		cls.PER_PAGE_IN_HOME=one.postnumberhome
		cls.PER_PAGE_IN_ADMIN=one.postnumberadmin
		cls.SHOW_TAG_NUMBER=one.showtagnumber
		cls.SHOW_TAGSEARCH_NUMBER=one.showtagsearchnumber
		cls.SHOW_LINK_NUMBER=one.showlinknumber
		cls.MEDIA_IN_ADMIN=one.showmediaadmin
		cls.COMMENT_IN_ADMIN=one.commentinadmin
		cls.COMMENT_IN_SIDEBAR=one.commentinsidebar
		cls.ANNOUNCELENGTH=one.announcelength
		cls.POST_ID=one.post_id
		if one.post_id!=-1:
			cls.ANNOUNCEMENT=SearchablePost.all().filter('post_id',one.post_id).get().content[0:cls.ANNOUNCELENGTH]


class Post(db.Model):
	title=db.StringProperty()
	content=db.TextProperty()
	create_date=db.IntegerProperty()
	update_time=db.IntegerProperty()
	tags = db.StringListProperty()
	saveonly=db.BooleanProperty()
	allowcomment=db.BooleanProperty()
	num_lookup=db.IntegerProperty()
	#id for each post ,since the original key value will change after put() 
	post_id=db.IntegerProperty()

	#used for cache
	PostCount=0
	AllCount=0

	@classmethod
	def get(cls,getall,PER_PAGE,beginpage):
		begin=(beginpage-1)*PER_PAGE
		if not getall:
			postlist=Post.all().filter('saveonly = ',False).order('-create_date').fetch(PER_PAGE,begin)
		else:
			postlist=Post.all().order('-create_date').fetch(PER_PAGE,begin)
		return postlist 
	

	@classmethod
	def getone(cls,post_id):
		post=Post.all().filter('post_id = ',int(post_id)).get()
		return post

	@classmethod
	def updatecache(cls):
		cls.PostCount=Post.all().filter('saveonly',False).count()
		cls.AllCount=Post.all().count()


	@classmethod
	def properid(cls):
		post=cls.all().order('-post_id').get()
		return post.post_id+1 if post else 1

	def settags(self,values):
		if not values:tags=[]
		if type(values)==type([]):
			tags=values
		else:
			tags=values.split(',')
			tags=[i.strip() for i in tags]

		if not self.tags:
			removelist=[]
			addlist=tags
		else:
			#search different  tags
			
			removelist=[n for n in self.tags if n not in tags]
			addlist=[n for n in tags if n not in self.tags]
		for v in removelist:
			Tag.remove(v)
		for v in addlist:
			Tag.add(v)
		self.tags=tags
	
	def remove(self):
		removelist=[n for n in self.tags]
		for n in removelist:
			Tag.remove(n)
		self.delete()

	def getjson(self):
		return json.dumps({
			'title':self.title,
			'content':self.content,
			'create_date':self.create_date,
			'update_time':self.update_time,
			'tags':self.tags,
			'post_id':self.post_id,
			'saveonly':self.saveonly,
			'allowcomment':self.allowcomment,
			'num_lookup':self.num_lookup
			})

class SearchablePost(becer.Model):
	title=db.StringProperty()
	content=db.TextProperty()
	create_date=db.IntegerProperty()
	update_time=db.IntegerProperty()
	tags = db.StringListProperty()
	saveonly=db.BooleanProperty()
	allowcomment=db.BooleanProperty()
	num_lookup=db.IntegerProperty()
	#id for each post ,since the original key value will change after put() 
	post_id=db.IntegerProperty()

	#used for cache
	PostCount=0
	AllCount=0


	@classmethod
	def SearchableProperties(cls):
		return[['content']]

	@classmethod
	def get(cls,getall,PER_PAGE,beginpage):
		begin=(beginpage-1)*PER_PAGE
		if not getall:
			postlist=SearchablePost.all().filter('saveonly = ',False).order('-create_date').fetch(PER_PAGE,begin)
		else:
			postlist=SearchablePost.all().order('-create_date').fetch(PER_PAGE,begin)
		return postlist 
	

	@classmethod
	def getone(cls,post_id):
		post=SearchablePost.all().filter('post_id = ',int(post_id)).get()
		return post

	@classmethod
	def updatecache(cls):
		cls.PostCount=SearchablePost.all().filter('saveonly',False).count()
		cls.AllCount=SearchablePost.all().count()


	@classmethod
	def properid(cls):
		post=SearchablePost.all().order('-post_id').get()
		return post.post_id+1 if post else 1

	def settags(self,values):
		if not values:tags=[]
		if type(values)==type([]):
			tags=values
		else:
			tags=values.split(',')
			tags=[i.strip() for i in tags]

		if not self.tags:
			removelist=[]
			addlist=tags
		else:
			#search different  tags
			
			removelist=[n for n in self.tags if n not in tags]
			addlist=[n for n in tags if n not in self.tags]
		for v in removelist:
			Tag.remove(v)
		for v in addlist:
			Tag.add(v)
		self.tags=tags
	
	def remove(self):
		removelist=[n for n in self.tags]
		for n in removelist:
			Tag.remove(n)
		self.delete()

	def getjson(self):
		return json.dumps({
			'title':self.title,
			'content':self.content,
			'create_date':self.create_date,
			'update_time':self.update_time,
			'tags':self.tags,
			'post_id':self.post_id,
			'saveonly':self.saveonly,
			'allowcomment':self.allowcomment,
			'num_lookup':self.num_lookup
			})


class Tag(db.Model):
	name=db.StringProperty()
	count=db.IntegerProperty()
	#used for cache,for the top User.SHOW_TAG_NUMBER
	CachedTag=[]

	@classmethod
	def updatecache(cls):
		cls.CachedTag=[]
		alltag=Tag.all().order('-count').fetch(User.SHOW_TAG_NUMBER)
		for item in alltag:
			cls.CachedTag.append({'name':item.name,'count':item.count})


	@classmethod
	def add(cls,item):
		if item:
			tag=Tag.all().filter("name",item).get()

			if tag:
				tag.count=tag.count+1
			else:
				tag=Tag(name=item,count=1)
			tag.put()

	@classmethod
	def remove(cls,item):
		if item:
			tag=Tag.all().filter("name",item).get()
			if tag:
				if tag.count>1:
					tag.count=tag.count-1
					tag.put()
				else :
					tag.delete()
	
class Comment(db.Model):
	comment_id=db.IntegerProperty()
	post_id=db.IntegerProperty()
	email=db.StringProperty()
	nickname=db.StringProperty()
	comment=db.TextProperty()
	create_date=db.IntegerProperty()
	ip=db.StringProperty()

	RecentComment=[]
	Allcount=0
	@classmethod
	def properid(cls):
		comment=Comment.all().order('-comment_id').get()
		comment_id=comment.comment_id+1 if comment else 1
		return comment_id

	def getjsonobj(self):
		return {"comment_id":self.comment_id,
						"post_id":self.post_id,
						"email":self.email,
						"nickname":self.nickname,
						"comment":self.comment,
						"create_date":self.create_date,
						"ip":self.ip
						}
	@classmethod
	def getall(cls,post_id,PER_PAGE,beginpage):
		logging.info('xxxxxxxxxx')
		logging.info(post_id)
		begin=(beginpage-1)*PER_PAGE
		if post_id==-1:
			commentlist=Comment.all().order('-create_date').fetch(PER_PAGE,begin)
		else:
			commentlist=Comment.all().filter('post_id',int(post_id)).order('-create_date').fetch(PER_PAGE,begin)

		return commentlist

	@classmethod
	def updatecache(cls):
		cls.Allcount=Comment.all().count()
		cls.RecentComment=Comment.all().order('-create_date').fetch(User.COMMENT_IN_SIDEBAR)

class Link(db.Model):
	name=db.StringProperty()
	link=db.StringProperty()
	description=db.StringProperty()
	create_date=db.IntegerProperty()
	display=db.BooleanProperty()
	link_id=db.IntegerProperty()
	
	#used for cache
	LinkListShow=[]
	LinkListAll=[]
	@classmethod
	def properid(cls):
		onelink=cls.all().order('-link_id').get()
		return onelink.link_id+1 if onelink else 1

	@classmethod
	def updatecache(cls):
		cls.LinkListAll=[]
		cls.LinkListShow=[]
		alllink=Link.all().fetch(User.SHOW_LINK_NUMBER)
		for each in alllink:
			cls.LinkListAll.append({'name':each.name,'link':each.link})
		
		showlink=Link.all().filter('display',True).fetch(User.SHOW_LINK_NUMBER)
		for each in showlink:
			cls.LinkListShow.append({'name':each.name,'link':each.link})
	
	@classmethod
	def deletelist(cls,idlist):
		for itemid in  idlist:
			one=Link.all().filter('link_id',itemid).get()
			one.delete()

	@classmethod
	def updatelist(cls,linklist):
		for item in linklist:
			one=Link.all().filter('link_id',item[0]).get()
			one.display=item[1]
			one.put()


class Media(db.Model):
	blobkey=db.StringProperty()
	name=db.StringProperty()
	size=db.IntegerProperty()
	create_date=db.IntegerProperty()
	display=db.BooleanProperty()
	
	Allcount=0
#	def __init__(self,blob,name,size,create_date,display):
#		db.Model.__init__(self,blob,name,size,create_date,display)
#		self.name=name
#		self.size=size
#		self.create_date=create_date
#		self.display=display
#		filename = files.blobstore.create(mime_type='application/octet-stream')
#		with files.open(filename,'a') as f:
#			f.write(blob)
#		self.blobkey=files.blobstore.get_blob_key(filename)

	def putcontent(self,blob):
		filename = files.blobstore.create(mime_type='application/octet-stream')
		with files.open(filename,'a') as f:
			f.write(blob)
		files.finalize(filename)
		self.blobkey=str(files.blobstore.get_blob_key(filename))
		#logging.debug(blob)
		#logging.debug(self.blobkey)



	@classmethod
	def updatecache(cls):
		cls.Allcount=Media.all().count()
	
	@classmethod
	def getall(cls,getall,PER_PAGE,beginpage):
		begin=(beginpage-1)*PER_PAGE
		if not getall:
			medialist=Media.all().filter('display',True).order('-create_date').fetch(PER_PAGE,begin)
		else:
			medialist=Media.all().order('-create_date').fetch(PER_PAGE,begin)
		return medialist

	@classmethod
#items in removelist means the specified blobkey
	def deletelist(cls,removelist):
		for item in removelist:
			one=Media.all().filter('blobkey',item).get()
			if one:
				blob=blobstore.BlobInfo.get(item)
				blob.delete()
				one.delete()

	@classmethod
	def updatemedia(cls,updatelist):
#whether or not to show the  media
		for item in updatelist:
			one=Media.all().filter('blobkey',item[0]).get()
			if one:
				one.display=item[1]
				one.put()
	
	@classmethod
#generate a url to upload files 
	def getuploadurl(cls):
		return blobstore.create_upload_url('/media/upload')

	@classmethod
#get the content of the blob
	def getmedia(cls,blobkey):
		blobreader=blobstore.BlobReader(blobkey)	
		data=blobreader.read()
		return data

	@classmethod
#get one instance by bolbkey
	def getmediainfo(cls,blobkey):
		return Media.all().filter('blobkey',blobkey).get()

#init database
Tag.updatecache()
#Post.updatecache()
SearchablePost.updatecache()
Link.updatecache()
Media.updatecache()
Comment.updatecache()
if User.all().count()==0:
	one=User(postnumberhome=settings.PER_PAGE_IN_HOME,
			postnumberadmin=settings.PER_PAGE_IN_ADMIN,
			showtagnumber=settings.SHOW_TAG_NUMBER,
			showtagsearchnumber=settings.SHOW_TAGSEARCH_NUMBER,
			showlinknumber=settings.SHOW_LINK_NUMBER,
			showmediaadmin=settings.MEDIA_IN_ADMIN,
			commentinadmin=settings.COMMENT_IN_ADMIN,
			commentinsidebar=settings.COMMENT_IN_SIDEBAR,
			announcelength=settings.ANNOUNCELENGTH,
			post_id=-1)
	one.put()
	logging.info('xxxxxxxxxxxxxxxxyxxx')
	User.updatecache(one)
else:
	User.updatecache()

