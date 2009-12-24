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
from zope import component
from zojax.cache.tag import Tag
from zojax.forum.interfaces import IForum, ITopic

ForumTag = Tag('forum')
TopicTag = Tag('forum.topic')


def forumMsgCacheHandler(ob, ev):
    forum = ob.__parent__.__parent__
    if IForum.providedBy(forum):
        ForumTag.update(forum)

    topic = ob.__parent__
    if ITopic.providedBy(topic):
        TopicTag.update(topic)


def forumTopicCacheHandler(ob, ev):
    forum = ob.__parent__
    if IForum.providedBy(forum):
        ForumTag.update(forum)
