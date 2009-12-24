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
from zope.traversing.browser import absoluteURL

from zojax.forum.browser import interfaces
from zojax.forum.interfaces import _, IForum, ITopic, IMessage


class ForumRSSFeedAction(object):
    component.adapts(IForum, interface.Interface)
    interface.implements(interfaces.IForumRSSFeedAction)

    weight = 99999
    title = _(u'RSS Feed')
    description = u''

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def url(self):
        return '%s/@@feeds/discussions'%absoluteURL(self.context, self.request)

    def isAvailable(self):
        return True


class MessagesRSSFeedAction(object):
    component.adapts(ITopic, interface.Interface)
    interface.implements(interfaces.IForumRSSFeedAction)

    weight = 99999
    title = _(u'RSS Feed')
    description = u''

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def url(self):
        return '%s/@@feeds/messages'%absoluteURL(self.context, self.request)

    def isAvailable(self):
        return True
