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
"""Batching Implementation (based on z3c.batching)

$Id$
"""
__docformat__ = 'restructuredtext'

from zope import interface
from zope.schema.fieldproperty import FieldProperty
from zope.interface.common.sequence import IFiniteSequence


class Batch(object):

    size = 0
    start = 0
    end = 0

    def __init__(self, context, start=0, size=20, reverse=False, batches=None):
        self.btree = context
        sequence = self.btree.keys()

        if reverse:
            self.sequence = ReverseSequence(sequence)
        else:
            self.sequence = sequence

        self.reverse = reverse

        length = len(self.btree)
        self.length = length

        # start
        self.start = start
        if length == 0:
            self.start = -1
        elif start >= length:
            raise IndexError('start index key out of range')

        # size
        self.size = size
        self._trueSize = size
        if start + size >= length:
            self._trueSize = length - start

        # end
        if length == 0:
            self.end = -1
        else:
            self.end = start + self._trueSize - 1

        if batches is None:
            batches = Batches(self)

        self.batches = batches

    @property
    def index(self):
        return self.start / self.size

    @property
    def number(self):
        return self.index + 1

    @property
    def total(self):
        total = self.length / self.size
        if self.length % self.size:
            total += 1
        return total

    @property
    def next(self):
        try:
            return self.batches[self.index + 1]
        except IndexError:
            return None

    @property
    def previous(self):
        idx = self.index - 1
        if idx >= 0:
            return self.batches[idx]
        return None

    @property
    def firstElement(self):
        return self.btree[self.sequence[self.start]]

    @property
    def lastElement(self):
        """See interfaces.IBatch"""
        return self.btree[self.sequence[self.end]]

    def __getitem__(self, key):
        """See zope.interface.common.sequence.IMinimalSequence"""
        if key >= self._trueSize:
            raise IndexError('batch index out of range')

        return self.btree[self.sequence[idx]]

    def __iter__(self):
        """See zope.interface.common.sequence.IMinimalSequence"""
        idx = 0
        start = self.start
        btree = self.btree

        while idx < self._trueSize:
            yield btree[self.sequence[start+idx]]
            idx = idx + 1

    def __len__(self):
        """See zope.interface.common.sequence.IFiniteSequence"""
        return self._trueSize

    def __repr__(self):
        return '<%s start=%i, size=%i>' % (
            self.__class__.__name__, self.start, self.size)


class Batches(object):
    interface.implements(IFiniteSequence)

    def __init__(self, batch):
        self.size = batch.size
        self.total = batch.total
        self.reverse = batch.reverse
        self.btree = batch.btree

        self._batches = {batch.index: batch}

    def __len__(self):
        return self.total

    def __getitem__(self, key):
        if key not in self._batches:
            if key < 0:
                key = self.total + key

            batch = Batch(
                self.btree, key*self.size, self.size, self.reverse, self)
            self._batches[batch.index] = batch

        try:
            return self._batches[key]
        except KeyError:
            raise IndexError(key)


class ReverseSequence(object):

    def __init__(self, sequence):
        self.sequence = sequence
        self.length = len(sequence)

    def __getitem__(self, idx):
        idx = self.length - idx - 1
        if idx < 0:
            raise KeyError(idx)
        return self.sequence[idx]
