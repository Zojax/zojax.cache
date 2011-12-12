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
from persistent import Persistent
from zope import interface
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty
from lovely.memcached.interfaces import IMemcachedClient

from interfaces import IMemcachedCache


class MemcachedCache(Persistent):
    interface.implements(IMemcachedCache)

    prefix = FieldProperty(IMemcachedCache['prefix'])

    @property
    def client(self):
        return getUtility(IMemcachedClient)

    def invalidate(self, ob, key=None):
        self.client.invalidate((self.prefix, ob), ns=key)

    def invalidateAll(self):
        self.client.invalidateAll()

    def query(self, ob, key=None, default=None):
        result = self.client.query((self.prefix, ob), ns=key)
        if result is None:
            return default
        else:
            return result

    def set(self, data, ob, key=None):
        self.client.set(data, (self.prefix,ob), ns=key)

    def getStatistics(self):
        return []