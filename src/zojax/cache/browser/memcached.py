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
from zope import interface, schema

from zojax.layoutform import Fields
from zojax.wizard.interfaces import ISaveable
from zojax.wizard.step import WizardStep, WizardStepForm
from zojax.statusmessage.interfaces import IStatusMessage
from zope.security.proxy import removeSecurityProxy


class IMemcachedCache(interface.Interface):
    pass

class MemcachedCacheEdit(WizardStepForm):
    interface.implements(ISaveable)

    fields = Fields(IMemcachedCache)

    def getContent(self):
        return self.context.memcached

    def applyChanges(self, data):
        self.context.memcached.update(**data)
        return True

    def isAvailable(self):
        return self.context.cachetype == u'memcached'


class MemcachedCacheStats(WizardStep):

    def update(self):
        request = self.request
        memcached = removeSecurityProxy(self.context.memcached)
        
        if 'memcached.invalidate' in request:
            changed = False
            for oid in request.get('objectIds', ()):
                ram.invalidate(oid)
                changed = True

            if changed:
                IStatusMessage(request).add(
                    u'Cache data has been invalidated.')

        if 'memcached.invalidateall' in request:
            memcached.invalidateAll()
            IStatusMessage(request).add(
                    u'Cache data has been invalidated.')

        self.stats = memcached.getStatistics()

        size = 0
        for rec in self.stats:
            size += rec['size']

        if size < 262144:
            self.size = '%0.2fKb'%(size/1024.0)
        else:
            self.size = '%0.2fMb'%(size/1048576.0)

    def isAvailable(self):
        return self.context.cachetype == u'memcached'
