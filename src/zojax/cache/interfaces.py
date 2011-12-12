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
from zope.app.cache.interfaces import ICache
from zope.component.interfaces import IObjectEvent
from zojax.widget.list.field import SimpleList
from zojax.widget.radio.field import RadioChoice
from zojax.widget.checkbox.field import CheckboxList

import vocabulary


class DoNotCache(Exception):
    """ do not cache method call """


class ICacheConfiglet(interface.Interface):
    """ cache configlet """

    cache = interface.Attribute('Currently selected cache')

    ram = interface.Attribute('RAM Cache')
    memcached = interface.Attribute('Memcached')

    enabled = schema.Bool(
        title = u'Enabled',
        description = u'Enabled site caching.',
        default = True,
        required = True)

    cachetype = RadioChoice(
        title = u'Cache type',
        description = u'Select cache type.',
        vocabulary = vocabulary.cacheTypes,
        default = u'ram',
        required = True)

    globalkeys = CheckboxList(
        title = u'Global keys',
        vocabulary = 'cache.global.keys',
        default = ['language', 'server'],
        required = False)

    requestvars = SimpleList(
        title = u'Request vars',
        description = u'Add value of request fields to cache key.',
        default = [],
        required = False)

    def query(id, key, default=None):
        """ return cached value """

    def set(data, id, key):
        """ set cache data """


class IBaseCache(ICache):
    
    def getStatistics():
        """Reports on the contents of a cache.

        The returned value is a sequence of dictionaries with the
        following keys:

          `path`, `hits`, `misses`, `size`, `entries`
        """

class IMemcachedCache(ICache, IBaseCache):

    prefix = schema.TextLine(
        title = u'Prefix',
        description = u'Memcached cache prefix.',
        default = u'cache',
        required = False)


class IKey(interface.Interface):
    """ key """

    def __call__(object, instance, *args, **kw):
        """ return dict or tuple for cacheKey.update """


class ITimeKey(IKey):
    """ time based key """

    hours = schema.List(
        title = u'Hours',
        required = True)

    minutes = schema.List(
        title = u'Minutes',
        required = True)


class ITagging(interface.Interface):

    def query(name, context=None):
        """ query tag vaue """

    def update(name, value, context=None):
        """ update tag value """


class ITag(IKey):
    """ cache tag """

    def query(context=None):
        """ query tag value """

    def update(context=None):
        """ update tag """


GLOBAL_KEYS = {}
""" all global keys in system """


class IGlobalKey(IKey):
    """ global key """


class IVisibleContext(interface.Interface):
    """ helper marker interface for content caching,
        this marker means that content and all sub content are visible to
        user that can see current context """

    
class IPurgeEvent(IObjectEvent):
    """Event which can be fired to purge a particular object.

    This event is not fired anywhere in this package. Instead, higher level
    frameworks are expected to fire this event when an object may need to be
    purged.

    It is safe to fire the event multiple times for the same object. A given
    object will only be purged once.
    """

class IPurgeable(interface.Interface):
    """Marker interface for content which should be purged when modified or
    removed.

    Event handlers are registered for ``IObjectModifiedEvent`` and
    ``IObjectRemovedEvent`` for contexts providing this interface. These are
    automatically purged.
    """

class IPurgePaths(interface.Interface):
    """Return paths to send as PURGE requests for a given object.

    The purging hook will look up named adapters from the objects sent to
    the purge queue (usually by an IPurgeEvent being fired) to this interface.
    The name is not significant, but is used to allow multiple implementations
    whilst still permitting per-type overrides. The names should therefore
    normally be unique, prefixed with the dotted name of the package to which
    they belong.
    """

    def getRelativePaths():
        """Return a list of paths that should be purged. The paths should be
        relative to the virtual hosting root, i.e. they should start with a
        '/'.

        These paths will be rewritten to incorporate virtual hosting if
        necessary.
        """

    def getAbsolutePaths():
        """Return a list of paths that should be purged. The paths should be
        relative to the domain root, i.e. they should start with a '/'.

        These paths will *not* be rewritten to incorporate virtual hosting.
        """
