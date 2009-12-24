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
import sys
from zope import interface
from zojax.cache import default
from zojax.cache.interfaces import DoNotCache


class cache(object):

    _undefined = object()
    _noneResult = '---- none ----'

    def __init__(self, objectId, *args):
        self.objectId = objectId
        self.keys = args

    def __call__(self, func):

        def decorated(instance, *args, **kw):
            cache = default.localData.cache

            objectId = self.objectId
            if callable(objectId):
                objectId = objectId(instance)

            try:
                cacheKey = {}
                for key in self.keys:
                    cacheKey.update(key(objectId, instance, *args, **kw))
            except DoNotCache:
                return func(instance, *args, **kw)

            try:
                for key in default.localData.keys:
                    cacheKey.update(key(objectId, instance, *args, **kw))
            except DoNotCache:
                return func(instance, *args, **kw)

            result = cache.query(objectId, cacheKey, self._undefined)

            if result == self._noneResult:
                return None

            if result is self._undefined:
                result = func(instance, *args, **kw)

                if result is None:
                    cache.set(self._noneResult, objectId, cacheKey)
                else:
                    cache.set(result, objectId, cacheKey)

            return result

        return decorated
