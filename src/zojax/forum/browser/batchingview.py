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
class BatchView(object):

    prev1 = None
    prev2 = None

    next1 = None
    next2 = None

    first = None
    first1 = None

    last = None
    last1 = None

    def update(self):
        context = self.context

        idx = [context.index]

        self.prev1 = context.previous
        if self.prev1 is not None:
            idx.append(self.prev1.index)
            self.prev2 = self.prev1.previous

            if self.prev2 is not None:
                idx.append(self.prev2.index)

        self.next1 = context.next
        if self.next1 is not None:
            idx.append(self.next1.index)
            self.next2 = self.next1.next

            if self.next2 is not None:
                idx.append(self.next2.index)

        if 0 not in idx:
            try:
                self.first = context.batches[0]
            except IndexError:
                pass

        if context.total-1 not in idx:
            try:
                self.last = context.batches[-1]
            except:
                pass

        if self.first is not None:
            if self.prev2.index > 1:
                self.first1 = context.batches[self.prev2.index/2]

        if self.last is not None:
            if self.next2.number < context.total-1:
                self.last1 = context.batches[
                    self.next2.index + (context.total - self.next2.number)/2]

    def render(self, batch_url=None):
        if self.context.total == 0:
            return u''

        if batch_url:
            self.batch_url = batch_url
        else:
            self.batch_url = self.request.URL

        return self.template()


class BatchPreview(object):

    def update(self):
        context = self.context

        if context.total > 1:
            batches = context.batches

            if context.total <= 5:
                self.batches = batches
            else:
                self.batches = [
                    batches[0], batches[1], batches[-2], batches[-1]]

    def render(self, batch_url=None):
        if self.context.total > 1:
            if batch_url:
                self.batch_url = batch_url
            else:
                self.batch_url = self.request.URL
            return self.template()
        else:
            return u''
