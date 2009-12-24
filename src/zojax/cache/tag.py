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
import time
from zope import interface
from zope.component import getUtility, getSiteManager
from zope.traversing.api import getPath, getParents
from zope.app.component.hooks import getSite
from zope.app.component.interfaces import ISite

import default as defaultmod
from interfaces import ITag, ITagging


class Tag(object):
    interface.implements(ITag)

    def __init__(self, name, genValue=time.time):
        self.name = name
        self.genValue = genValue

        sm = getSiteManager()
        if sm.queryUtility(ITag, name) is not None:
            raise ValueError('Tag "%s" already registered.'%name)
        sm.registerUtility(self, name=name)

    def query(self, context=None, default=None):
        global tagging
        return tagging.query(self.name, context, default)

    def update(self, context):
        global tagging
        tagging.update(self.name, self.genValue(), context)

    def __call__(self, id, instance, *args, **kw):
        global tagging
        val = tagging.query(self.name, instance.context)
        if val:
            return (('tag:%s'%self.name, val),)
        return ()


class SiteTag(Tag):

    def query(self, context=None, default=None):
        global tagging
        return tagging.query(self.name, getSite(), default)

    def update(self, context=None):
        global tagging
        tagging.update(self.name, self.genValue(), getSite())

    def __call__(self, id, instance, *args, **kw):
        global tagging
        val = tagging.query(self.name, getSite())
        if val:
            return (('tag:%s'%self.name, val),)
        return ()


class ContextTag(Tag):

    def update(self, context):
        global tagging

        name = self.name
        value = self.genValue()

        # update self
        tagging.update(name, value, context)

        # update in parents
        for context in getParents(context):
            tagging.update(name, value, context)


class Tagging(object):
    interface.implements(ITagging)

    def query(self, name, context=None, default=0.0):
        data = defaultmod.localData.cache.query('zojax:cache:tagging', (), {})
        if context is None:
            return data.get((name,), default)
        else:
            return data.get((name, getPath(context)), default)

    def update(self, name, value, context=None):
        data = defaultmod.localData.cache.query('zojax:cache:tagging', (), {})

        if context is None:
            key = (name,)
        else:
            key = (name, getPath(context))

        default = data.get(key, 0.0)
        if value > default:
            data[key] = value
            defaultmod.localData.cache.set(data, 'zojax:cache:tagging', ())


tagging = Tagging()
