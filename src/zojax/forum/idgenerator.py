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
from persistent import Persistent
from BTrees.Length import Length
from zope import interface, component
from zope.cachedescriptors.property import Lazy
from zope.security.proxy import removeSecurityProxy
from zope.app.container.contained import NameChooser
from zope.app.container.interfaces import IContainerNamesContainer

from zojax.forum.interfaces import IIdGenerator


class IdGenerator(Persistent):
    interface.implements(IIdGenerator, IContainerNamesContainer)

    @Lazy
    def _next_id(self):
        next = Length(1)
        self._p_changed = True
        return next

    @property
    def nextId(self):
        id = self._next_id()
        self._next_id.change(1)
        return u'%0.5d'%id


class NameChooser(NameChooser):
    component.adapts(IIdGenerator)

    def __init__(self, context):
        self.context = context

    def chooseName(self, name, object):
        return removeSecurityProxy(self.context).nextId
