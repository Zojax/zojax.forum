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
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import IDCTimes

from zojax.cache.view import cache
from zojax.cache.keys import ContextModified
from zojax.ownership.interfaces import IOwnership
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.formatter.utils import getFormatter


class TopicForumView(object):

    lastmessage = None

    def update(self):
        topic = self.context
        request = self.request
        formatter = getFormatter(request, 'fancyDatetime', 'medium')

        name = topic.__name__
        owner = IOwnership(topic).owner
        profile = IPersonalProfile(owner)
        space = getattr(profile, 'space', None)

        self.name = name
        self.replies = len(topic)-1
        self.owner = getattr(profile, 'title', '')
        self.avatar = profile is not None and profile.avatarUrl(request) or '#',
        self.personal = '%s/'%(space and absoluteURL(space, request) or '',)

        message = topic.lastMessage

        if message is not None:
            owner = IOwnership(message).owner
            profile = IPersonalProfile(owner, None)
            space = getattr(profile, 'space', None)

            self.lastmessage = {
                'date': formatter.format(IDCTimes(message).modified),
                'owner': getattr(profile, 'title', ''),
                'personal': '%s/'%(space and absoluteURL(space,request) or '',),
                'avatar': profile is not None and profile.avatarUrl(request) or '#',
                'url': '%s/%s/'%(name, message.__name__)}

    @cache('forum.topicforumview', ContextModified)
    def updateAndRender(self):
        return super(TopicForumView, self).updateAndRender()
