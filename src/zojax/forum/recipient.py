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
from zope import interface, component, event
from zope.component import getUtility, queryMultiAdapter
from zope.proxy import sameProxiedObjects
from zope.security import checkPermission
from zope.security.management import queryInteraction
from zope.app.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent
from zojax.forum.interfaces import IForum
from zojax.mailin.interfaces import IRecipient
from zojax.mailin.utils import getSubject, getParsedBody
from zojax.forum.interfaces import TOPIC_FIRST_MESSAGE
from zojax.richtext.field import RichTextData
from zojax.content.type.interfaces import IContentType
from zojax.content.draft.interfaces import IDraftContainer, IDraftContentType


class ForumRecipient(object):
    component.adapts(IForum)
    interface.implements(IRecipient)

    def __init__(self, context):
        self.context = context

    def process(self, message):
        title = getSubject(message)
        text = RichTextData(*getParsedBody(message))

        if message.has_key('In-Reply-To'):
            self.reply(title, text, message)
        else:
            self.discussion(title, text, message)

    def reply(self, title, text, message):
        oid = message['In-Reply-To'].split('@', 1)[0].split('.', 1)[0][1:]
        try:
            topic = getUtility(IIntIds).getObject(int(oid))
        except:
            return

        if not sameProxiedObjects(topic.__parent__, self.context):
            return

        if checkPermission('zojax.forum.AddMessage', topic):
            ct = getUtility(IContentType, 'forum.message').__bind__(topic)
            ct.add(ct.create(title=title, text=text))

    def discussion(self, title, text, message):
        if checkPermission('zojax.forum.AddTopic', self.context):
            ct = getUtility(IContentType, 'forum.topic').__bind__(self.context)
            topic = ct.add(ct.create(title=title))
            topic[TOPIC_FIRST_MESSAGE].text = text
            return

        elif checkPermission('zojax.forum.SubmitTopic', self.context):
            interaction = queryInteraction()
            if interaction is not None and interaction.participations:
                request = interaction.participations[0]

                ct = getUtility(IDraftContentType, 'forum.topic')
                container = queryMultiAdapter(
                    (request.principal, ct), IDraftContainer)

                if container is not None:
                    draft = ct.add(ct.create(), container)
                    draft.content.title = title
                    draft.content[TOPIC_FIRST_MESSAGE].text = text
                    draft.location = getUtility(IIntIds).getId(self.context)
                    draft.submit()
                    event.notify(ObjectModifiedEvent(draft))
                    event.notify(ObjectModifiedEvent(draft.content))

        #tool.replyError(PROJECTNAME, error_templates[1],
        #                {'forum_title': self.Title(),
        #                 'forum_url': self.absolute_url(),
        #                 }, msg, self)
        #log(
        #"ForumMailReceiver: Member doesn't have permission to add new topic")
