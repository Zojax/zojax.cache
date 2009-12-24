##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface

from ram import RAMCache
from memcached import MemcachedCache
from interfaces import ICacheConfiglet


class CacheConfiglet(object):
    interface.implements(ICacheConfiglet)

    @property
    def ram(self):
        cache = self.data.get('ramcache')
        if cache is None:
            cache = RAMCache()
            self.data['ramcache'] = cache

        return cache

    @property
    def memcached(self):
        cache = self.data.get('memcached')
        if cache is None:
            cache = MemcachedCache()
            self.data['memcached'] = cache

        return cache

    @property
    def cache(self):
        if self.cachetype == u'ram':
            return self.ram
        else:
            return self.memcached

    def query(self, id, key, default=None):
        if not self.enabled:
            return default
        return self.cache.query(id, key, default)

    def set(self, data, id, key):
        if self.enabled:
            self.cache.set(data, id, key)


class NoCache(object):
    interface.implements(ICacheConfiglet)

    def query(self, id, key, default=None):
        return default

    def set(self, data, id, key):
        pass


class DefaultCacheConfiglet(object):
    interface.implements(ICacheConfiglet)

    def __init__(self):
        self.cache = RAMCache()

    def query(self, id, key, default=None):
        return self.cache.query(id, key, default)

    def set(self, data, id, key):
        self.cache.set(data, id, key)


noCache = NoCache()
defaultCacheConfiglet = DefaultCacheConfiglet()
