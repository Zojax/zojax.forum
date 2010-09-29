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
from zope import interface
from zope.security import checkPermission
from zope.component import getUtility, getMultiAdapter
from zope.security.proxy import removeSecurityProxy
from zope.dublincore.interfaces import ICMFDublinCore
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.formatter.utils import getFormatter
from zojax.layout.pagelet import BrowserPagelet
from zojax.ownership.interfaces import IOwnership

from zojax.forum.interfaces import ISignatures, IForumProduct

from interfaces import IMessageView, IPrincipalInformation


class MessageView(object):

    def __call__(self):
        msg = self.context

        name = msg.__name__
        idx = int(name)

        size = getUtility(IForumProduct).topic_page_size

        bstart = (int(round(float(idx)/size + 0.5)) - 1)*size
        self.request.response.redirect('../?bstart=%s#%s'%(bstart, name))


class MessagePreview(BrowserPagelet):
    interface.implements(IMessageView)

    signature = u''

    def update(self, **kw):
        request = self.request
        message = removeSecurityProxy(self.context)

        if kw:
            for attr, value in kw.items():
                setattr(self, attr, value)
        else:
            self.formatter = getFormatter(request, 'fancyDatetime', 'medium')
            self.userinfos = {}

        owner = IOwnership(message).owner

        if message.signature:
            sigs = ISignatures(owner)
            self.signature = getattr(sigs, 'signature%s'%message.signature, '')

        self.text = message.text.cooked
        self.created = self.formatter.format(ICMFDublinCore(message).created)

        userinfo = self.userinfos.get(owner.id)
        if userinfo is None:
            userinfo = getMultiAdapter(
                (owner, request), IPrincipalInformation)
            userinfo.update()
            userinfo = userinfo.render()
            self.userinfos[owner.id] = userinfo

        self.userinfo = userinfo

    def contextUrl(self):
        if checkPermission('zojax.ModifyContent', self.context):
            return '%s/context.html'%self.context.__name__

    def replyUrl(self):
        if checkPermission('zojax.forum.AddTopic', self.context.__parent__):
            return '%s/context.html'%self.context.__name__

    def deleteUrl(self):
        if checkPermission('zojax.forum.DeleteTopic', self.context.__parent__):
            return '%s/context.html'%self.context.__name__
