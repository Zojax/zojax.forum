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
import types
from zope import interface
from zope.proxy import removeAllProxies
from zope.component import getUtility, getAdapter, getMultiAdapter
from zope.security import checkPermission
from zope.security.proxy import removeSecurityProxy
from zope.session.interfaces import ISession
from zope.traversing.browser import absoluteURL
from zope.publisher.interfaces import NotFound
from zope.dublincore.interfaces import ICMFDublinCore
from zope.app.intid.interfaces import IIntIds
from zope.app.security.interfaces import IUnauthenticatedPrincipal

from zojax.cache.view import cache
from zojax.cache.keys import Context
from zojax.batching.batch import Batch
from zojax.batching.interfaces import IBatchView
from zojax.catalog.interfaces import ICatalog
from zojax.content.notifications.interfaces import IContentNotification
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.forum.browser.cache import ForumTag
from zojax.forum.interfaces import _, IForumProduct, IForum

SESSIONKEY = 'zojax.forum.search'


class Forum(object):

    menu = False
    searching = False
    searchResults = None

    def update(self):
        context = self.context
        request = self.request

        self.noIcon = not bool(self.context.icon)

        principal = self.request.principal
        if not IUnauthenticatedPrincipal.providedBy(principal):
            self.menu = True

            self.submitTopic = \
                checkPermission('zojax.forum.AddTopic', context) or \
                checkPermission('zojax.forum.SubmitTopic', context)

            notifications = getAdapter(context, IContentNotification, 'forum')
            self.subscribed = notifications.isSubscribed(principal.id)

        if len(self.context) > 1:
            self.searching = True

        data = ISession(request)[SESSIONKEY]
        forum = removeAllProxies(context)
        key = getUtility(IIntIds).getId(forum)

        if 'form.button.search' in request:
            searchableText = request['form.searchforum']
            data[key] = (searchableText, True)

        if 'form.button.clear' in request:
            searchableText = None
            if key in data:
                del data[key]

        else:
            searchtext, searching = data.get(key, (u'', False))
            if searchtext and searching:
                searchableText = searchtext
            else:
                searchableText = None

        if searchableText:
            query = {'searchableText': searchableText,
                     'type': {'any_of': ('forum.message',)},
                     'traversablePath': {'any_of': (forum,)},
                     'noPublishing': True, 'noSecurityChecks': True}

            try:
                results = getUtility(ICatalog).searchResults(**query)
            except Exception, e:
                IStatusMessage(self.request).add(e, 'error')
                return

            self.total = len(results)
            self.searchableText = searchableText
            self.searchResults = Batch(results, size=20, request=request)


def ForumViewBatchStart(oid, instance, *args, **kw):
    return {'bstart': instance.batch.start,
            'bpages': len(instance.batch.batches)}


class ForumView(object):

    def __init__(self, context, request):
        super(ForumView, self).__init__(context, request)

        product = getUtility(IForumProduct)

        forum = removeSecurityProxy(context)
        self.batch = Batch(
            forum.topics, size=product.forum_page_size,
            context=context, request=request)

        self.topics = forum.topics

    def update(self):
        self.bottomLinks = len(self.topics) > 5

        batchView = getMultiAdapter(
            (self.batch, self, self.request), IBatchView)
        batchView.update()
        self.batchView = batchView.render()

    @cache('forum.view', ForumTag, ForumViewBatchStart, Context)
    def updateAndRender(self):
        return super(ForumView, self).updateAndRender()


class ForumIcon(object):

    def __call__(self):
        if self.context.icon:
            return self.context.icon.show(self.request)

        raise NotFound(self, 'icon', self.request)


class ForumSubscribe(object):

    def __call__(self):
        request = self.request
        principal = request.principal

        if not IUnauthenticatedPrincipal.providedBy(principal):
            notifications = getAdapter(
                self.context, IContentNotification, 'forum')
            if notifications.isSubscribed(principal.id):
                notifications.unsubscribe(principal.id)
                IStatusMessage(request).add(_('You have been unsubscribed.'))
            else:
                notifications.subscribe(principal.id)
                IStatusMessage(request).add(_('You have been subscribed.'))

        request.response.redirect('.')
        return u''


class ReverseSequence(object):

    def __init__(self, sequence):
        self.sequence = sequence
        self.length = len(sequence)

    def __getitem__(self, idx):
        if isinstance(idx, types.SliceType):
            length = self.length

            start = idx.start or 0
            stop = idx.stop or length
            if stop > length:
                stop = length

            getitem = self.__getitem__
            return [getitem(idx) for idx in range(start, stop)]

        if idx < 0:
            idx = - idx - 1
        else:
            idx = self.length - idx - 1

        if idx < 0:
            raise IndexError('list index out of range')

        return self.sequence[idx]

    def __len__(self):
        return self.length
