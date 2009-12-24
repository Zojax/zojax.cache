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
from zope.proxy import removeAllProxies
from zope.security import checkPermission
from zope.component import getUtility
from zope.traversing.api import getPath
from zope.dublincore.interfaces import IDCTimes

from interfaces import IKey, IVisibleContext

_marker = object()


def Path(object, instance, *args, **kw):
    return {'path': getPath(instance)}


def Principal(object, instance, *args, **kw):
    return {'principal': instance.request.principal.id}


def PrincipalAndContext(object, instance, *args, **kw):
    return {'principal': instance.request.principal.id,
            'context': getPath(instance.context)}


def VisibleContext(object, instance, *args, **kw):
    if IVisibleContext.providedBy(instance.context):
        return {'context': getPath(instance.context)}
    else:
        return {'principal': instance.request.principal.id,
                'context': getPath(instance.context)}


def Context(object, instance, *args, **kw):
    return {'context': getPath(instance.context)}


def ContextModified(object, instance, *args, **kw):
    key = {'context': getPath(instance.context)}

    times = IDCTimes(instance.context, None)
    if times is not None:
        key['modified'] = times.modified

    return key


class Attributes(object):

    def __init__(self, *attrs, **kw):
        self.attrs = attrs
        self.prefix = kw.get('prefix', u'')

    def __call__(self, object, instance, *args, **kw):
        key = {}
        prefix = self.prefix
        context = removeAllProxies(instance.context)

        for attr in self.attrs:
            value = getattr(context, attr, _marker)
            if value is not _marker:
                key['%s%s'%(prefix, attr)] = value

        return key


class PermissionsAndContext(object):

    def __init__(self, *permissions, **kw):
        self.permissions = permissions

    def __call__(self, object, instance, *args, **kw):
        context = instance.context

        return {'context': getPath(context),
                'permissions': tuple(((p, checkPermission(p, context)) for p \
                                in self.permissions))}
