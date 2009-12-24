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
from zope.component import getSiteManager
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from interfaces import GLOBAL_KEYS, IGlobalKey


_marker = object()


class GlobalKey(object):
    interface.implements(IGlobalKey)

    def __init__(self, name, title=u'', description=u''):
        self.name = name
        self.title = title
        self.description = description

        sm = getSiteManager()
        if sm.queryUtility(IGlobalKey, name) is not None:
            raise ValueError('RequestKey "%s" already registered.'%name)
        sm.registerUtility(self, name=name)

        GLOBAL_KEYS[name] = self

    def __call__(self, objectId, instance, *args, **kw):
        raise NotImlemented('__call__')


def GlobalKeysVocabulary(context):
    terms = []
    for key in GLOBAL_KEYS.values():
        term = SimpleTerm(key.name, key.name, key.title)
        term.description = key.description
        terms.append((key.title, term))

    terms.sort()
    return SimpleVocabulary([term for _t, term in terms])
