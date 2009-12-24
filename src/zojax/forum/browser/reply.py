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
""" reply form

$Id$
"""
from zope import schema
from zope.event import notify
from zope.component import getUtility, getMultiAdapter
from zope.lifecycleevent import ObjectCreatedEvent
from zope.app.container.interfaces import INameChooser

from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.layoutform import button, Fields, PageletForm
from zojax.ownership.interfaces import IOwnership
from zojax.preferences.interfaces import IPreferenceGroup
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.forum.message import Message
from zojax.forum.interfaces import _, IMessage
from zojax.forum.browser.interfaces import IMessageView


class ReplyForm(PageletForm):

    fields = Fields(IMessage['title'], IMessage['text'])

    preview = False

    @property
    def label(self):
        return _("Post new message (${title})",
                 mapping={'title': self.context.title})

    def getContent(self):
        data = {'title': self.context.title,
                'text': u''}

        if not data['title'].lower().startswith('re:'):
            data['title'] = u'Re: '+ data['title']

        return data

    def createMessage(self, data):
        msg = Message(data['title'])

        # set attributes
        for name, field in schema.getFields(IMessage).items():
            field.set(msg, data.get(name, field.default))

        # set message signature
        prefs = getUtility(IPreferenceGroup, 'forum.sigs').__bind__()
        msg.signature = prefs.default

        notify(ObjectCreatedEvent(msg))
        return msg

    @button.buttonAndHandler(_("Reply"))
    def handleAdd(self, action):
        data, errors = self.extractData()

        if errors:
            IStatusMessage(self.request).add(self.formErrorsMessage, 'error')
            return

        msg = self.createMessage(data)

        # add to container
        topic = self.context
        name = INameChooser(topic).chooseName('', msg)
        topic[name] = msg

        if IMessage.providedBy(self.context):
            self.redirect('./')
        else:
            self.redirect('./%s/'%msg.__name__)

    @button.buttonAndHandler(_("Preview"))
    def handlePreview(self, action):
        data, errors = self.extractData()

        if errors:
            IStatusMessage(self.request).add(self.formErrorsMessage, 'error')
            return

        msg = self.createMessage(data)
        IOwnership(msg).owner = self.request.principal

        view = getMultiAdapter((msg, self.request), IMessageView)
        view.update()
        self.preview = view.template()
