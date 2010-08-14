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
from email.Utils import formataddr

from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds

from zojax.ownership.interfaces import IOwnership
from zojax.mailin.interfaces import IMailInDestination
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.forum.interfaces import IForumProduct, TOPIC_FIRST_MESSAGE


class NotificationMail(object):

    def update(self):
        super(NotificationMail, self).update()

        topic = self.context
        self.topic = topic
        message = self.contexts[0]
        forum = topic.__parent__
        request = self.request
        self.url = '%s/'%absoluteURL(message, request)
        self.message = message
        self.forum = forum
        self.forumurl = absoluteURL(forum, request)

        principal = IOwnership(message).owner

        profile = IPersonalProfile(principal)
        if profile.email:
            author = profile.title
            self.author = author
            self.addHeader(u'From', formataddr((author, profile.email),))
        else:
            self.author = principal.title or principal.id

        self.site = getSite()

        destination = IMailInDestination(forum)
        if destination.enabled:
            self.addHeader(u'To', destination.address)
            self.addHeader(u'Reply-To', destination.address)
            self.addHeader(u'List-Post', u'<mailto:%s>'%destination.address)
        else:
            self.addHeader(u'To', formataddr((self.author, profile.email),))

        ids = getUtility(IIntIds)
        msgId = ids.getId(message)
        topicId = ids.getId(topic)

        if message.__name__ == TOPIC_FIRST_MESSAGE:
            self.messageId = u'<%s@zojax.net>'%(topicId)
        else:
            self.messageId = u'<%s.%s@zojax.net>'%(topicId, msgId)

        self.addHeader(u'List-Id', u'%s'%forum.title)
        self.addHeader(u'List-Unsubscribe', u'%s/@@notifications'%self.forumurl)
        self.addHeader(u'List-Subscribe', u'%s/@@notifications'%self.forumurl)
        self.addHeader(u'List-Archive', u'%s/'%self.forumurl)

        self.addHeader(u'In-Reply-To', u'<%s@zojax.net>'%topicId)
        self.addHeader(u'References', u'<%s@zojax.net>'%topicId)

    def text(self):
        text = self.message.text.cooked

        if u'src="@@content.attachment/' in text:
            s = u'src="%s/@@content.attachment/'%absoluteURL(
                getSite(), self.request)
            text = text.replace(u'src="@@content.attachment/', s)

        return text

    @property
    def subject(self):
        return u'%s: %s: %s'%(self.forum.title, self.topic.title, self.message.title)
