#!/usr/bin/env python
#coding:utf-8
"""
	decorators.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.

Decorators for URL handlers
"""


from functools import wraps
from google.appengine.api import users
from flask import redirect, request, abort,g,session
from application.settings import BLOGUSERMAIL
from google.appengine.api import memcache
import logging,settings

def admin_required(func):
	"""Requires standard login credentials"""
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if g.user and g.user.email() ==  BLOGUSERMAIL:
			return func(*args, **kwargs)
		else :
			return redirect(users.create_login_url(request.url))
	return decorated_view

def login_required(func):
	@wraps(func)
	def decorated_view(*args,**kargs):
		if g.user:
			return func(*args,**kargs)
		else :
			return redirect(users.create_login_url(request.url)) 
	return decorated_view

def decorator_with_args(decorator_to_enhance):
    """ 
    This function is supposed to be used as a decorator.
    It must decorate an other function, that is intended to be used as a decorator.
    Take a cup of coffee.
    It will allow any decorator to accept an arbitrary number of arguments,
    saving you the headache to remember how to do that every time.
    
    This comes from http://stackoverflow.com/questions/739654/understanding-python-decorators
    """
 
    # We use the same trick we did to pass arguments
    def decorator_maker(*args, **kwargs) :
 
        # We create on the fly a decorator that accepts only a function
        # but keeps the passed arguments from the maker .
        def decorator_wrapper(func) :
 
            # We return the result of the original decorator, which, after all, 
            # IS JUST AN ORDINARY FUNCTION (which returns a function).
            # Only pitfall : the decorator must have this specific signature or it won't work :
            return decorator_to_enhance(func, *args, **kwargs)
 
        return decorator_wrapper
 
    return decorator_maker
 

#if settings.DEBUG==True:
#	@decorator_with_args
#	def cached(func, *args, **kwargs):
#	    """
#	    Caches the result of a method for a specified time in seconds
#	    
#	    Use it as:
#	      
#	      @cached(time=1200)
#	      def functionToCache(arguments):
#	      
#	    """
#	    def wrapper(*pars):
#	        key = func.__name__ + '_' + '_'.join([str(par) for par in pars])
#	        logging.info('keykeykey............')
#	        logging.info(key)
#	        val = memcache.get(key)
#	        logging.debug('Cache lookup for %s, found: %s', key, val != None)
#	        if not val:
#	            val = func(*pars)
#	            memcache.set(key, val, time=kwargs['time'])
#	        return val
#	        
#	    return wrapper
#else: 
#	@decorator_with_args
#	def cached(func,*args,**kargs):
#	
#		def wrapper(*pars):
#			val=func(*pars)
#			return val
#		return wrapper
	

def cached(time=600, key=None):
    """
    A decorator to memoize the results of a function call in memcache. Use this
    in preference to doing your own memcaching, as this function avoids version
    collisions etc...

    Note that if you are not providing a key (or a function to create one) then your
    arguments need to provide consistent str representations of themselves. Without an
    implementation you could get the memory address as part of the result - "<... object at 0x1aeff0>"
    which is going to vary per request and thus defeat the caching.
    
    Usage:
    @auto_cache
    get_by_type(type):
        return MyModel.all().filter("type =", type)
    
    :param expiration: Number of seconds before the value is forced to re-cache, 0
    for indefinite caching
    
    :param key: Option manual key, use in combination with expiration=0 to have
    memcaching with manual updating (eg by cron job). Key can be a func(*args, **kwargs)

    :rtype: Memoized return value of function
    """
    
    def wrapper(fn):
        def cache_decorator(*args, **kwargs):

            #dev_bypass = common.IS_SDK or common.IS_REMOTE_DEV
            #if dev_bypass and not ENABLE_DEV_AUTO_CACHE:
            #    return fn(*args, **kwargs)

            mc_key = None
            if key:
                if callable(key):
                    mc_key = key(*args, **kwargs)
                else:
                    mc_key = key
            else:
                mc_key = '%s:%s-%s-%s' % ("auto_cache", fn.func_name, str(args), str(kwargs))
            
            #if ENABLE_VERSIONED_AUTO_CACHE:
             #   mc_key += "-" + common.CURRENT_VERSION_ID            
                                
            result = memcache.get(mc_key)
            
            if not result:
                result = fn(*args, **kwargs)

                try:
                    memcache.set(mc_key, result, time=time)
                except ValueError, e:
                    logging.critical("Recevied error from memcache", exc_info=e)

            return result
        return cache_decorator
    return wrapper
