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
import time, types
from persistent import Persistent
from BTrees.Length import Length
from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree

from zope import interface
from interfaces import ITopics


class Topics(Persistent):
    interface.implements(ITopics)

    def __init__(self):
        self.topics = OOBTree()
        self.btopics = IOBTree()
        self.__len = Length(0)

    def __len__(self):
        return self.__len()

    def __iter__(self):
        return iter(xrange(len(self)))

    def __getitem__(self, key):
        topics = self.topics
        keys = topics.keys()

        if isinstance(key, types.SliceType):
            length = len(self)

            start = key.start or 0
            stop = key.stop or length
            if stop > length:
                stop = length

            getitem = self.__getitem__
            return [getitem(idx) for idx in range(start, stop)]
        else:
            if key < 0:
                key = - key - 1
            else:
                key = len(self) - key - 1

            return topics[keys[key]]

    def append(self, topic):
        self.remove(topic)

        id = int(topic.__name__)

        idx = time.time()
        while idx in self.topics:
            idx = idx + 0.00001

        self.topics[idx] = topic
        self.btopics[id] = idx
        self.__len.change(1)

    def remove(self, topic):
        id = int(topic.__name__)

        if id in self.btopics:
            idx = self.btopics[id]
            del self.btopics[id]
            del self.topics[idx]
            self.__len.change(-1)

    def next(self, topic):
        """ return next topic """
        id = int(topic.__name__)

        idx = self.btopics.get(id)
        if idx is not None:
            idx = idx - 0.000001

            try:
                idx = self.topics.maxKey(idx)
            except ValueError:
                return None

            return self.topics.get(idx)

    def previous(self, topic):
        """ return prev topic """
        id = int(topic.__name__)

        idx = self.btopics.get(id)
        if idx is not None:
            idx = idx + 0.000001

            try:
                idx = self.topics.minKey(idx)
            except ValueError:
                return None

            return self.topics.get(idx)
