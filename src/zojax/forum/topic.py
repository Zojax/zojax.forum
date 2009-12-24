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
""" simple forum topic implementation

$Id$
"""
from BTrees.IOBTree import IOBTree

from zope import event, interface, component
from zope.proxy import removeAllProxies
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.intid.interfaces import IIntIdAddedEvent
from zope.app.container.interfaces import IObjectRemovedEvent

from zojax.content.type.container import ContentContainer
from zojax.content.type.interfaces import IUnremoveableContent
from zojax.content.type.interfaces import IDraftedContent

from interfaces import IForum
from interfaces import TOPIC_FIRST_MESSAGE, ITopic, IMessage

from message import Message
from idgenerator import IdGenerator


class Topic(IdGenerator, ContentContainer):
    interface.implements(ITopic)

    def __init__(self, *args, **kw):
        super(Topic, self).__init__(*args, **kw)

        self.messages = IOBTree()

    @property
    def lastMessage(self):
        try:
            return self.messages[self.messages.maxKey()]
        except ValueError:
            return None

    def __setitem__(self, key, message):
        super(Topic, self).__setitem__(key, message)

        self.messages[int(message.__name__)] = message

        if key != TOPIC_FIRST_MESSAGE  and IForum.providedBy(self.__parent__):
            self.__parent__.count_replies.change(1)

    def __delitem__(self, key):
        msg = self[key]

        del self.messages[int(msg.__name__)]

        super(Topic, self).__delitem__(key)

        if key != TOPIC_FIRST_MESSAGE and IForum.providedBy(self.__parent__):
            self.__parent__.count_replies.change(-1)

    def __repr__(self):
        cls = self.__class__
        return "<%s.%s '%s'>"%(cls.__module__, cls.__name__, self.__name__)


@component.adapter(ITopic, IIntIdAddedEvent)
def topicIdAddedHandler(topic, tevent):
    if TOPIC_FIRST_MESSAGE not in topic:
        msg = Message(topic.title)
        interface.directlyProvides(msg, IUnremoveableContent)

        event.notify(ObjectCreatedEvent(msg))
        topic[TOPIC_FIRST_MESSAGE] = msg


@component.adapter(ITopic, IObjectModifiedEvent)
def topicModifiedHandler(topic, tevent):
    if not IDraftedContent.providedBy(topic):
        topic = removeAllProxies(topic)
        topic.__parent__.topics.append(topic)

        msg = topic[TOPIC_FIRST_MESSAGE]
        msg.title = topic.title


@component.adapter(ITopic, IObjectRemovedEvent)
def topicRemovedHandler(topic, tevent):
    if not IDraftedContent.providedBy(topic):
        topic = removeAllProxies(topic)
        topic.__parent__.topics.remove(topic)
