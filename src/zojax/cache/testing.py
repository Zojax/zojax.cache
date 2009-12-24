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
from rwproperty import getproperty, setproperty
from zojax.cache import default
from zojax.cache.ram import RAMCache

originalTime = time.time
originalLocaltime = time.localtime


class TimeOverrides(object):

    def __init__(self):
        self.curentTime = time.time()
        self.currentLocaltime = time.localtime(curentTime)

    def setUp(*args):
        time.time = self.__time
        time.localtime = self.__localtime

    def tearDown(*args):
        time.time = originalTime
        time.localtime = originalLocaltime

    def setTime(self, time):
        pass

    def setLocaltime(self, localtime):
        pass

    def change(self, minutes=0, seconds=0):
        pass

    def __time(self):
        return self.currentTime

    def __localtime(self, value=None):
        if value is not None:
            return originalLocaltime(value)
        return self.currentLocaltime


class LocalData(object):

    _old_values = ((), (), None)

    def __init__(self, keys, cache, requestvars):
        self._values = (keys, cache, requestvars)

    @getproperty
    def keys(self):
        return self._values[0]
    @setproperty
    def keys(self, value):
        pass

    @getproperty
    def cache(self):
        return self._values[1]
    @setproperty
    def cache(self, value):
        pass

    @getproperty
    def requestvars(self):
        return self._values[2]
    @setproperty
    def requestvars(self, value):
        pass

origLocalData = default.localData


def setUpCache(*args, **kw):
    default.localData = LocalData((), RAMCache(), ())


def tearDownCache(*args, **kw):
    default.localData = origLocalData
