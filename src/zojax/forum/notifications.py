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
from zope import interface, component
from zope.app.container.interfaces import IObjectAddedEvent
from zojax.subscription.interfaces import ISubscriptionDescription
from zojax.content.draft.interfaces import IDraftPublishedEvent
from zojax.content.notifications.utils import sendNotification
from zojax.content.notifications.notification import Notification

from interfaces import _, TOPIC_FIRST_MESSAGE
from interfaces import IMessage, ITopic, IForum, IForumNotification


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


@component.adapter(ITopic, IDraftPublishedEvent)
def topicPublished(topic, ev):
    sendNotification('forum', topic, topic[TOPIC_FIRST_MESSAGE])


@component.adapter(IMessage, IObjectAddedEvent)
def messageAdded(message, ev):
    sendNotification('forum', message.__parent__, message)
