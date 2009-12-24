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
from zope.security import checkPermission
from zope.security.proxy import removeSecurityProxy
from zope.dublincore.interfaces import ICMFDublinCore
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.publisher.interfaces import NotFound

from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.table.table import Table
from zojax.table.column import Column

from zojax.formatter.utils import getFormatter
from zojax.content.type.interfaces import IOrder
from zojax.ownership.interfaces import IOwnership
from zojax.forum.interfaces import _, IForum, IForumFolder
from zojax.principal.profile.interfaces import IPersonalProfile


from interfaces import IForumsTable


class FolderView(object):

    def listFolders(self):
        folders = []
        for key, folder in IOrder(self.context).items():
            if IForumFolder.providedBy(folder) and \
                    checkPermission('zope.View', folder):
                yield {'name': folder.__name__,
                       'title': folder.title,
                       'description': folder.description,
                       'ob': folder}


class FolderIcon(object):

    def __call__(self):
        if self.context.icon:
            return self.context.icon.show(self.request)

        raise NotFound(self, 'icon', self.request)


class ForumsTable(Table):
    interface.implements(IForumsTable)
    component.adapts(IForumFolder,
                     interface.Interface,
                     interface.Interface)

    title = _('Forums listing')

    pageSize = 0
    enabledColumns = ('icon', 'title', 'stats', 'info')
    disabledColumns = ()

    def initDataset(self):
        order = IOrder(self.context)

        forums = []

        for key, forum in order.items():
            if IForum.providedBy(forum) and checkPermission('zope.View', forum):
                forum = removeSecurityProxy(forum)
                forums.append(forum)

        self.dataset = forums


class IconColumn(Column):
    component.adapts(IForumFolder, interface.Interface, IForumsTable)

    weight = 0
    name = 'icon'
    title = _('Icon')
    cssClass = 'f-icon'

    def render(self):
        forum = self.content

        if forum.icon:
            url = absoluteURL(forum, self.request)
            return '<img src="%s/icon" title="%s" />'%(
                url, forum.title)


class TitleColumn(Column):
    component.adapts(IForumFolder, interface.Interface, IForumsTable)

    weight = 10

    name = 'title'
    title = _('Title')
    cssClass = 'f-title'

    template = ViewPageTemplateFile('forumtitle.pt')

    def query(self, default=None):
        forum = self.content
        return {'url': absoluteURL(forum, self.request),
                'title': forum.title,
                'description': forum.description}


class StatsColumn(Column):
    component.adapts(IForumFolder, interface.Interface, IForumsTable)

    weight = 20

    name = 'stats'
    title = _('Stats')
    cssClass = 'f-stats'

    template = ViewPageTemplateFile('forumstats.pt')

    def query(self, default=('', '')):
        return self.content.count_replies(), self.content.count_topics


class LastPostColumn(Column):
    component.adapts(IForumFolder, interface.Interface, IForumsTable)

    weight = 30

    name = 'lastPost'
    title = _('Last post')
    cssClass = 'f-info'

    template = ViewPageTemplateFile('forumlastpost.pt')

    def query(self, default=None):
        forum = self.content
        url = absoluteURL(self.context, self.request)
        siteUrl = absoluteURL(getSite(), self.request)
        formatter = getFormatter(self.request, 'fancyDatetime', 'medium')

        topic = forum.lastTopic
        if topic is not None:
            message = topic.lastMessage
            owner = IOwnership(message).owner
            profile = IPersonalProfile(owner)
            space = profile.space

            return {
                'date': formatter.format(
                    ICMFDublinCore(message).modified),
                'owner': profile.title,
                'profile': '%s/'%(space is not None and absoluteURL(space, self.request) or siteURL),
                'avatar': profile.avatarUrl(self.request),
                'title': topic.title,
                'url': '%s/%s/%s/%s/'%(
                    url, forum.__name__, topic.__name__, message.__name__)}
