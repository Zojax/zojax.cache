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
    >>> class Test(object):
    ...     __name__ = 'test'

    >>> ob = Test()
    >>> PortletId()(ob), PortletId(' :postfix')(ob)
    (u'portlet: test', u'portlet: test :postfix')
    >>> PageletId()(ob), PageletId(' :pageletpostfix')(ob)
    (u'pagelet: test', u'pagelet: test :pageletpostfix')
    >>> PageElementId()(ob), PageElementId(' :pepostfix')(ob)
    (u'pageelement: test', u'pageelement: test :pepostfix')

$Id$
"""

class CallableObjectId(object):

    prefix = u''

    def __init__(self, postfix=u''):
        self.postfix = postfix

    def __call__(self, instance):
        return u'%s%s%s'%(self.prefix, instance.__name__, self.postfix)


class PortletId(CallableObjectId):

    prefix = u'portlet: '


class PageElementId(CallableObjectId):

    prefix = u'pageelement: '


class PageletId(CallableObjectId):

    prefix = u'pagelet: '
