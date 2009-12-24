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
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.security.proxy import removeSecurityProxy
from zojax.content.space.interfaces import IContentSpace
from zojax.content.space.workspace import WorkspaceFactory

import interfaces
from forum import Forum
from folder import BaseForumFolder
from interfaces import _


class ForumWorkspace(Forum):
    interface.implements(interfaces.IForumWorkspace)

    @property
    def space(self):
        return self.__parent__


class ForumsWorkspace(BaseForumFolder):
    interface.implements(interfaces.IForumsWorkspace)

    @property
    def space(self):
        return self.__parent__


class ForumWorkspaceFactory(WorkspaceFactory):
    component.adapts(IContentSpace)
    interface.implements(interfaces.IForumWorkspaceFactory)

    name = 'forum'
    title = _(u'Forum')
    description = _(u'Check this box if you want only one forum on your site.')
    weight = 1000
    factory = ForumWorkspace

    @property
    def title(self):
        if self.isInstalled():
            return self.space['forum'].title
        else:
            return _(u'Forum')


class ForumsWorkspaceFactory(WorkspaceFactory):
    component.adapts(IContentSpace)
    interface.implements(interfaces.IForumWorkspaceFactory)

    name = 'forums'
    description = _(u'Check this box if you want 2 or more forums on your site.')
    weight = 1001
    factory = ForumsWorkspace

    @property
    def title(self):
        if self.isInstalled():
            return self.space['forums'].title
        else:
            return _(u'Forums')
