#!/usr/bin/env python
#coding:utf-8
"""
	task.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""
from flask import Blueprint,render_template,g,request
from application.models import * 
from application.decorators import admin_required
import json,logging,urllib

from google.appengine.api import memcache
task=Blueprint('task',__name__,template_folder="../templates")

from google.appengine.api import search

@task.route('/dotask')
@admin_required
def dotask():
	one=User.all().get()
	one.delete()
	return "update successfully"

@task.route('/addpost')
@admin_required
def addpost():
	document=search.Document(fields=[search.HtmlField(name="content",value=u"核心提示：到底是什么导致全球变暖？英国科学家们给出了一个“匪夷所思”的答案：生活在中生代的食草类恐龙排出大量甲烷气体，是全球变暖的重要因素。这一研究结果于近期发表在《当代生物学》杂志上")])
	search.Index(name="Post").put(document)
	document=search.Document(fields=[search.HtmlField(name="content",value=u"核心提示：据媒体调查称，2009年住建部曾对全国城市饮用水水质状况做普查，但至今未公布数据结果。多位业内人士称，此次检测结果实际合格率仅50%左右。调查显示全国城市供水管网质量普遍低劣，不符国标的灰口铸铁管占一半。目前，北京上海等大城市饮用水仍无法直饮。")])
	search.Index(name="Post").put(document)

	return "ok"

@task.route('/search/<searchtag>')
@admin_required
def dosearch(searchtag):
	logging.info(searchtag)
	searchtag=urllib.unquote(searchtag)
	results=search.Index(name="Post").search(searchtag)
	return str(results)
	

#@task.route('/movetopost')
#def movetopost():
#	allpost=SPost.all().fetch(1000)
#	for one in allpost:
#		newone=Post(
#				title=one.title,
#					content=one.content,
#					create_date=one.create_date,
#					update_time=one.update_time,
#					tags=one.tags,
#					saveonly=one.saveonly,
#					allowcomment=one.allowcomment,
#					num_lookup=one.num_lookup,
#					post_id=one.post_id
#					)
#		logging.info('xxxxxx')
#		logging.info(newone.title)
#		newone.put_into()
#	return "ok"
