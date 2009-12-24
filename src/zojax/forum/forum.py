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
from BTrees.Length import Length

from zope import interface
from zojax.richtext.field import RichTextProperty
from zojax.filefield.field import FileFieldProperty
from zojax.content.type.container import ContentContainer

from zojax.forum.topics import Topics
from zojax.forum.interfaces import IForum
from zojax.forum.idgenerator import IdGenerator


class Forum(IdGenerator, ContentContainer):
    interface.implements(IForum)

    text = RichTextProperty(IForum['text'])
    icon = FileFieldProperty(IForum['icon'])

    def __init__(self, *args, **kw):
        super(Forum, self).__init__(*args, **kw)

        self.topics = Topics()
        self.count_replies = Length()

    @property
    def count_topics(self):
        return len(self)

    @property
    def lastTopic(self):
        topics = self.topics.topics
        try:
            return topics[topics.minKey()]
        except ValueError:
            return None

    @property
    def firstTopic(self):
        topics = self.topics.topics
        try:
            return topics[topics.maxKey()]
        except ValueError:
            return None
