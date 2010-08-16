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
from zojax.content.type.interfaces import IDraftedContent
"""

$Id$
"""
from zope import interface, component
from zope.app.container.interfaces import IObjectAddedEvent

from zojax.subscription.interfaces import ISubscriptionDescription,\
    SubscriptionException
from zojax.content.draft.interfaces import IDraftPublishedEvent
from zojax.content.notifications.utils import sendNotification
from zojax.content.notifications.notification import Notification
from zojax.ownership.interfaces import IOwnership

from interfaces import _, TOPIC_FIRST_MESSAGE
from interfaces import IMessage, ITopic, IForum, IForumNotification, \
                       ITopicNotification


class ForumNotification(Notification):
    component.adapts(IForum)
    interface.implementsOnly(IForumNotification)

    type = u'forum'
    title = _(u'Forum')
    description = _(u'Forum discussions.')


class ForumNotificationDescription(object):
    interface.implements(ISubscriptionDescription)

    title = _(u'Forum')
    description = _(u'Forum discussions.')


class TopicNotification(Notification):
    component.adapts(ITopic)
    interface.implementsOnly(ITopicNotification)

    type = u'forum.topic'
    title = _(u'Forum discussion')
    description = _(u'Forum discussion messages.')


class TopicNotificationDescription(object):
    interface.implements(ISubscriptionDescription)

    title = _(u'Forum discussion')
    description = _(u'Forum discussion messages.')



@component.adapter(ITopic, IDraftPublishedEvent)
def topicPublished(topic, ev):
    sendNotification('forum', topic, topic[TOPIC_FIRST_MESSAGE])
    notification = component.getAdapter(topic, ITopicNotification, 'forum.topic')
    try:
        if not notification.isSubscribed(IOwnership(topic).owner.id):
            notification.subscribe()
    except SubscriptionException:
        pass
    sendNotification('forum.topic', topic, topic[TOPIC_FIRST_MESSAGE])


@component.adapter(IMessage, IObjectAddedEvent)
def messageAdded(message, ev):
    if IDraftedContent.providedBy(message.__parent__):
        return
    sendNotification('forum', message.__parent__, message)
    notification = component.getAdapter(message.__parent__, ITopicNotification, 'forum.topic')
    try:
        if not notification.isSubscribed():
            notification.subscribe()
    except SubscriptionException:
        pass
    sendNotification('forum.topic', message.__parent__, message)
