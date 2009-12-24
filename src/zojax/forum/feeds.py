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
import time, rfc822
from zope import interface, component
from zope.component import getUtility, getUtilitiesFor
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import IDCTimes

from zojax.content.feeds.rss2 import RSS2Feed
from zojax.catalog.interfaces import ICatalog
from zojax.ownership.interfaces import IOwnership
from zojax.content.space.interfaces import ISpace
from zojax.principal.profile.interfaces import IPersonalProfile

from interfaces import _, IForum, ITopic, IForumRSSFeed, TOPIC_FIRST_MESSAGE


class TopicsRSSFeed(RSS2Feed):
    component.adapts(ISpace)
    interface.implementsOnly(IForumRSSFeed)

    name = u'discussions'
    title = _(u'Forum topics')
    description = _(u'List of recently changed forum discussions in current space '
                    u'and all sub spaces.')

    def items(self):
        request = self.request

        results = getUtility(ICatalog).searchResults(
            traversablePath={'any_of':(self.context,)},
            type={'any_of': ('forum.topic',)},
            sort_order='reverse', sort_on='modified',
            isDraft={'any_of': (False,)})[:30]

        for item in results:
            url = absoluteURL(item, request)

            info = {
                'title': item.title,
                'description': item[TOPIC_FIRST_MESSAGE].text.cooked,
                'guid': '%s/'%url,
                'pubDate': rfc822.formatdate(time.mktime(
                        IDCTimes(item).modified.timetuple())),
                'isPermaLink': True}

            principal = IOwnership(item).owner
            if principal is not None:
                profile = IPersonalProfile(principal)
                info['author'] = u'%s (%s)'%(profile.email, profile.title)

            yield info


class ForumRSSFeed(TopicsRSSFeed):
    component.adapts(IForum)

    description = _(u'List of recently changed discussion in this forum.')


class MessagesRSSFeed(RSS2Feed):
    component.adapts(ISpace)
    interface.implementsOnly(IForumRSSFeed)

    name = u'messages'
    title = _(u'Forum messages')
    description = _(u'List of recently posted forum messages in current space '
                    u'and all sub spaces.')

    def items(self):
        request = self.request

        results = getUtility(ICatalog).searchResults(
            traversablePath={'any_of':(self.context,)},
            type={'any_of': ('forum.message',)},
            sort_order='reverse', sort_on='modified',
            isDraft={'any_of': (False,)})[:30]

        for item in results:
            url = absoluteURL(item, request)

            info = {
                'title': item.title,
                'description': item.text.cooked,
                'guid': '%s/'%url,
                'pubDate': rfc822.formatdate(time.mktime(
                        IDCTimes(item).modified.timetuple())),
                'isPermaLink': True}

            principal = IOwnership(item).owner
            if principal is not None:
                profile = IPersonalProfile(principal)
                info['author'] = u'%s (%s)'%(profile.email, profile.title)

            yield info


class ForumMessagesRSSFeed(MessagesRSSFeed):
    component.adapts(IForum)

    description = _(u'List of recently posted messages in this forum.')


class TopicMessagesRSSFeed(MessagesRSSFeed):
    component.adapts(ITopic)

    description = _(u'List of recently posted messages in this discussion.')
