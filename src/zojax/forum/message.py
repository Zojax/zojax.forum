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
""" IMessage implementation

$Id$
"""
from zope import interface, component, event
from zope.proxy import removeAllProxies
from zope.dublincore.interfaces import IDCTimes
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.richtext.field import RichTextProperty
from zojax.content.type.item import PersistentItem

from interfaces import IMessage


class Message(PersistentItem):
    interface.implements(IMessage)

    signature = 1
    text = RichTextProperty(IMessage['text'])

    def __repr__(self):
        cls = self.__class__
        return "<%s.%s '%s'>"%(cls.__module__, cls.__name__, self.__name__)


@component.adapter(IMessage, IObjectModifiedEvent)
def messageModifiedHandler(message, _event):
    message = removeAllProxies(message)

    topic = message.__parent__

    IDCTimes(topic).modified = IDCTimes(message).modified
    event.notify(ObjectModifiedEvent(topic))
