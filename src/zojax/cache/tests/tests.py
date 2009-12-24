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
import os
import unittest, doctest
from persistent import Persistent
from zope import interface, component, event
from zope.location import Location
from zope.annotation import IAttributeAnnotatable
from zope.app.rotterdam import Rotterdam
from zope.app.testing import functional
from zope.app.component.hooks import setSite
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.cache.view import cache


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


class TestPage(object):

    @cache('test.page')
    def updateAndRender(self):
        return u'Static text for testing'


zojaxCache = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxCache', allow_teardown=True)


def FunctionalDocFileSuite(*paths, **kw):
    layer = zojaxCache

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite("cache.txt"),
            FunctionalDocFileSuite("tag.txt"),
            FunctionalDocFileSuite("timekey.txt"),
            FunctionalDocFileSuite("key.txt"),
            FunctionalDocFileSuite("testbrowser.txt"),
            doctest.DocTestSuite(
                'zojax.cache.ids',
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            ))
