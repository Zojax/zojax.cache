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
from BTrees.IIBTree import IIBTree

from zope import interface
from interfaces import ITimeKey

eachHour = (-1,)
each2hours = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22)
each4hours = (0, 4, 8, 12, 16, 20)
each6hours = (0, 6, 12, 18)
each8hours = (0, 8, 16)

eachMinute = (-1,)
each0minute = (0,)
each2minutes = tuple(range(0, 60, 2))
each3minutes = tuple(range(0, 60, 3))
each4minutes = tuple(range(0, 60, 4))
each5minutes = tuple(range(0, 60, 5))
each10minutes = tuple(range(0, 60, 10))
each15minutes = tuple(range(0, 60, 15))
each20minutes = tuple(range(0, 60, 20))
each30minutes = tuple(range(0, 60, 30))
each40minutes = tuple(range(0, 60, 40))
each50minutes = tuple(range(0, 60, 50))


class TimeKey(object):
    interface.implements(ITimeKey)

    def __init__(self, hours=eachHour, minutes=each0minute, name='time'):
        self.hours = IIBTree([(i, 1) for i in hours])
        self.minutes = IIBTree([(i, 1) for i in minutes])
        self.name = name

    def __call__(self, *args, **kw):
        now = time.localtime()

        minute = now[4]
        if not (self.minutes.has_key(-1) or self.minutes.has_key(minute)):
            minute = self.minutes.maxKey(minute)

        hour = now[3]
        if not (self.hours.has_key(-1) or self.hours.has_key(hour)):
            hour = self.hours.maxKey(hour)

        return {self.name: time.mktime(now[:3] + (hour, minute, 0, 0, 0, 0))}


class TagTimeKey(TimeKey):

    def __init__(self, tag, minutes=each10minutes, name='tagtime'):
        self.minutes = IIBTree([(i, 1) for i in minutes])

        self.tag = tag
        self.name = name

    def __call__(self, objectId, instance, *arg, **kw):
        tag = self.tag.query(instance.context)
        if not tag:
            return ()

        tag = time.localtime(tag)

        minute = tag[4]
        if not (self.minutes.has_key(-1) or self.minutes.has_key(minute)):
            minute = self.minutes.maxKey(minute)

        try:
            minute2 = self.minutes.minKey(minute+1)
            time2 = time.mktime(tag[:4] + (minute2, 0, 0, 0, 0))
        except ValueError:
            time2 = time.mktime(tag[:4] + (0, 0, 0, 0, 0)) + 3600

        if time2 < time.time():
            return {'%s:%s'%(self.name, self.tag.name): time2}

        return {'%s:%s'%(self.name, self.tag.name):
                    time.mktime(tag[:4] + (minute, 0, 0, 0, 0))}
