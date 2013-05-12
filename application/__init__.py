#!/usr/bin/env python
#coding:utf-8
"""
Initialize Flask app

"""

from prepare import createapp
#from flaskext.gae_mini_profiler import GAEMiniProfiler
from gae_mini_profiler import profiler, templatetags
app = createapp()

 # Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app = profiler.ProfilerWSGIMiddleware(app)

# Enable profiler (enabled in non-production environ only)
#GAEMiniProfiler(app)

# Pull in URL dispatch routes
#import urls

#gae-mini-profiler
