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
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zojax.content.notifications.interfaces import IContentNotification
from zojax.statusmessage.interfaces import IStatusMessage
""" topic view

$Id$
"""
from zope import interface
from zope.security import checkPermission
from zope.security.proxy import removeSecurityProxy
from zope.component import getUtility, getMultiAdapter

from zojax.batching.batch import Batch
from zojax.batching.interfaces import IBatchView
from zojax.layoutform import Fields, PageletEditSubForm
from zojax.formatter.utils import getFormatter
from zojax.preferences.interfaces import IPreferenceGroup
from zojax.content.draft.interfaces import IDraftedContent

from zojax.cache.view import cache
from zojax.cache.keys import ContextModified

from zojax.forum.interfaces import TOPIC_FIRST_MESSAGE
from zojax.forum.interfaces import IForum, IForumProduct, IMessage

from cache import TopicTag
from interfaces import IMessageView
from zojax.forum.interfaces import _


class Topic(object):

    reply = None

    def update(self):
        super(Topic, self).update()

        context = self.context
        request = self.request

        context = removeSecurityProxy(context)

        if not IDraftedContent.providedBy(context) and \
                checkPermission('zojax.forum.AddMessage', context):
            self.reply = getMultiAdapter((context, request), name='reply.html')

        info = {'replies': len(context)-1, 'next': None, 'prev': None}

        forum = context.__parent__

        if IForum.providedBy(IForum):
            topics = forum.topics

            next = topics.next(context)
            if next is not None:
                info['prev'] = {'name': next.__name__,
                                'title': next.title}

            prev = topics.previous(context)
            if prev is not None:
                info['next'] = {'name': prev.__name__,
                                'title': prev.title}

        self.topicInfo = info

        if self.reply is not None:
            self.reply.update()
            if self.reply.isRedirected:
                self.redirect()


def TopicBatchTag(oid, instance, *args, **kw):
    return {'bstart': (instance.batch.start, len(instance.batch)),
            'bpages': len(instance.batch.batches)}


class TopicPage(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

        size = getUtility(IForumProduct).topic_page_size
        messages = removeSecurityProxy(context.messages)

        batch = Batch(
            messages.keys(), size=size, context=context, request=request)

        self.batch = batch
        self.messages = messages

    def update(self):
        super(TopicPage, self).update()

        view = getMultiAdapter(
            (self.batch, self.context, self.request), IBatchView)
        view.update()
        self.batchView = view.render()

    def listMessages(self):
        request = self.request
        messages = self.messages

        data = {'signatures': getUtility(IPreferenceGroup, 'forum.sigs'),
                'formatter': getFormatter(request, 'fancyDatetime', 'medium'),
                'userinfos': {}}

        for msgId in self.batch:
            message = messages[msgId]
            view = getMultiAdapter((message, request), IMessageView)
            view.update(**data)
            yield view.template()

    @cache('forum.topicview', TopicBatchTag, TopicTag, ContextModified)
    def updateAndRender(self):
        return super(TopicPage, self).updateAndRender()


class TopicMessageEdit(PageletEditSubForm):

    fields = Fields(IMessage).omit('title')

    def getContent(self):
        return self.context[TOPIC_FIRST_MESSAGE]


class TopicSubscribe(object):

    def __call__(self):
        request = self.request
        principal = request.principal

        if not IUnauthenticatedPrincipal.providedBy(principal):
            notifications = getAdapter(
                self.context, IContentNotification, 'topic')
            if notifications.isSubscribed(principal.id):
                notifications.unsubscribe(principal.id)
                IStatusMessage(request).add(_('You have been unsubscribed.'))
            else:
                notifications.subscribe(principal.id)
                IStatusMessage(request).add(_('You have been subscribed.'))

        request.response.redirect('.')
        return u''
