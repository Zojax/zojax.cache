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
from threading import local

from zope import component
from zope.component import getUtility
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.component.interfaces import ISite
from zope.app.publication.interfaces import \
    IBeforeTraverseEvent, IEndRequestEvent

from interfaces import ICacheConfiglet
from globalkey import GLOBAL_KEYS, GlobalKey
from configlet import noCache, defaultCacheConfiglet


class LocalData(local):

    keys = ()
    cache = noCache
    requestvars = ()

    _old_values = ((), (), None)

localData = LocalData()


def requestVarsKey(objectId, instance, *args, **kw):
    global localData
    request = instance.request

    key = {}
    for var in localData.requestvars:
        if var in request:
            key['request:%s'%var] = request[var]

    return key

@component.adapter(ISite, IBeforeTraverseEvent)
def beforeTraverseHandler(site, event):
    global localData

    localData._old_values = (
        localData.keys, localData.cache, localData.requestvars)

    configlet = getUtility(ICacheConfiglet)
    if configlet.enabled:
        localData.keys = [GLOBAL_KEYS[kname] for kname in configlet.globalkeys]
        localData.cache = configlet.cache
        localData.requestvars = configlet.requestvars
        if localData.requestvars:
            localData.keys.append(requestVarsKey)
    else:
        localData.keys = ()
        localData.cache = noCache
        localData.requestvars = ()


@component.adapter(IEndRequestEvent)
def endRequestHandler(event):
    global localData

    localData.keys, localData.cache, localData.requestvars = \
        localData._old_values


class LanguageKey(GlobalKey):

    def __call__(self, objectId, instance, *args, **kw):
        lang = IUserPreferredLanguages(instance.request, None)
        if lang is not None:
            lang = lang.getPreferredLanguages()
            if lang:
                return {'request:%s'%self.name: lang[0]}

        return ()


languageKey = LanguageKey(
    'language', u'User preferred language',
    u'Users preferred language. This key usefull in site policy allow to change preferred language.')


class ServerKey(GlobalKey):

    def __call__(self, objectId, instance, *args, **kw):
        request = instance.request
        if IBrowserRequest.providedBy(request):
            return {'request:SERVER_NAME':
                        (request.get('SERVER_NAME', u''),
                         request.get('SERVER_PORT', u''),
                         request.getApplicationURL(),)}
        else:
            return ()

serverKey = ServerKey(
    'server', u'Server name',
    u'This key usefull when site accessed with different urls.')
