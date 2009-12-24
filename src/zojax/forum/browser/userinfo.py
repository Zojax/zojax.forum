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
from zope.traversing.browser import absoluteURL
from zojax.principal.profile.interfaces import IPersonalProfile


class UserInformation(object):

    avatar = None
    profile = None

    def update(self):
        context = self.context
        request = self.request

        profile = IPersonalProfile(context)
        space = profile.space

        if space:
            self.profile = '%s/'%absoluteURL(space, request)

        self.title = profile.title
        self.avatar = profile.avatarUrl(request)
