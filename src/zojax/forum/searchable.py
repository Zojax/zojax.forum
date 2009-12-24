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
from zope.index.text.interfaces import ISearchableText
from zojax.content.type.searchable import ContentSearchableText

from interfaces import ITopic, IMessage, TOPIC_FIRST_MESSAGE


class TopicSearchableText(ContentSearchableText):
    component.adapts(ITopic)

    def getSearchableText(self):
        text = super(TopicSearchableText, self).getSearchableText()

        if TOPIC_FIRST_MESSAGE in self.content:
            message = MessageSearchableText(self.content[TOPIC_FIRST_MESSAGE])
            return text + message.getSearchableText()
        else:
            return text


class MessageSearchableText(ContentSearchableText):
    component.adapts(IMessage)

    def getSearchableText(self):
        text = super(MessageSearchableText, self).getSearchableText()

        return text + getattr(self.content.text, 'text', u'')
