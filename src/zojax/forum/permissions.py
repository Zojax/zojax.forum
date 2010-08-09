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
from zope import component, interface
from zope.component import queryAdapter
from zojax.content.space.interfaces import ISpace, IWorkspaceFactory
from zojax.content.permissions.permission import ContentPermission


class ForumPermission(ContentPermission):

    def isAvailable(self):
        wf = queryAdapter(self.context, IWorkspaceFactory, 'forum')
        if wf is None:
            wf = queryAdapter(self.context, IWorkspaceFactory, 'forums')

        if wf is None or not self.context.isEnabled(wf):
            return

        return super(ForumPermission, self).isAvailable()


class ForumsPermission(ContentPermission):

    def isAvailable(self):
        wf = queryAdapter(self.context, IWorkspaceFactory, 'forums')
        if wf is None or not self.context.isEnabled(wf):
            return

        return super(ForumsPermission, self).isAvailable()


@component.adapter(ISpace, interface.Interface)
def forumPermissionContentTypes(context, permissions):
    if ('zojax.forum.AddTopic' in permissions or
        'zojax.forum.DeleteTopic' in permissions or
        'zojax.forum.SubmitTopic' in permissions or
        'zojax.forum.AddMessage' in permissions or
        'zojax.forum.SubmitMessage' in permissions):
        return 'content.forum', 'workspace.forum', 'workspace.forums'
