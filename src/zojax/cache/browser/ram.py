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


class IRAMCache(interface.Interface):

    maxEntries = schema.Int(
        title = u'Maximum cached entries',
        default = 1000,
        required = True)

    maxAge = schema.Int(
        title = u'Maximum age of cached entries (seconds)',
        default = 3600,
        required = True)

    cleanupInterval = schema.Int(
        title = u'Time between cache cleanups (seconds)',
        default = 300,
        required = True)


class RAMCacheEdit(WizardStepForm):
    interface.implements(ISaveable)

    fields = Fields(IRAMCache)

    def getContent(self):
        ram = self.context.ram
        return {'maxEntries': ram.maxEntries,
                'maxAge': ram.maxAge,
                'cleanupInterval': ram.cleanupInterval}

    def applyChanges(self, data):
        self.context.ram.update(**data)
        return True

    def isAvailable(self):
        return self.context.cachetype == u'ram'


class RAMCacheStats(WizardStep):

    def update(self):
        request = self.request
        ram = self.context.ram

        if 'ram.invalidate' in request:
            changed = False
            for oid in request.get('objectIds', ()):
                ram.invalidate(oid)
                changed = True

            if changed:
                IStatusMessage(request).add(
                    u'Cache data has been invalidated.')

        self.stats = ram.getStatistics()

        size = 0
        for rec in self.stats:
            size += rec['size']

        if size < 262144:
            self.size = '%0.2fKb'%(size/1024.0)
        else:
            self.size = '%0.2fMb'%(size/1048576.0)

    def isAvailable(self):
        return self.context.cachetype == u'ram'
