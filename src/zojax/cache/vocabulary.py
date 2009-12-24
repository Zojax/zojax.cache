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
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


tp1 = SimpleTerm(u'ram', 'ram', 'RAM Cache')
tp1.description = u'This cache store data in ram.'

tp2 = SimpleTerm(u'memcached', 'memcached', 'Memcached')
tp2.description = u'This cache store data in memcached server.'

cacheTypes = SimpleVocabulary((tp1, tp2))
