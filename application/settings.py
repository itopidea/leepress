#!/usr/bin/env python
#decoding:utf-8
"""
	settings.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.

Configuration for Flask app

Important: Place your keys in the secret_keys.py module, 
           which should be kept out of version control.

"""

import os
from secret_keys import CSRF_SECRET_KEY, SESSION_KEY

DEBUG_MODE = False

# Auto-set debug mode based on App Engine dev environ
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG_MODE = True

DEBUG = DEBUG_MODE

# Set secret keys for CSRF protection
SECRET_KEY = CSRF_SECRET_KEY
CSRF_SESSION_KEY = SESSION_KEY

CSRF_ENABLED = True



CACHE_TYPE = "simple"
CACHE_DEFAULT_TIMEOUT = 300

#THEME = 'default'
#THEME_PATHS=os.path.join(os.path.abspath('.'),'application/themes')
ACCEPT_LANGUAGES = ['en', 'zh']

BABEL_DEFAULT_LOCALE = 'zh'
BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'

BLOGUSERMAIL="fzleee@gmail.com"

NOT_LOGIN_TAG=(('Home','/'),('Login','/login'),)
ADMIN_TAG=(('Home','/'),('Manage','/admin'),('NewPost','/admin/post'),('Database','/_ah/admin/datastore'))
NONE_LOGIN_TAG=(('Home','/'))
ADMIN_TOOL_BAR=(('写文章','/admin/post'),('文章','/page'),('设置','/setting'),('链接','/link'),('资源','/media'))


#how many posts are shown in the home page
PER_PAGE_IN_HOME=15
PER_PAGE_IN_ADMIN=20

#how many tags are shown in home page
SHOW_TAG_NUMBER=20
#how many tags are shown in tag search page 
SHOW_TAGSEARCH_NUMBER=20
SHOW_LINK_NUMBER=10
MEDIA_IN_ADMIN=10
COMMENT_IN_ADMIN=20
COMMENT_IN_SIDEBAR=10
ANNOUNCELENGTH=200
