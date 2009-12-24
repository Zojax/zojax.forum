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
""" vocabularies

$Id$
"""
from interfaces import _
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


Signatures = SimpleVocabulary((
        SimpleTerm(1, '1', _(u'Signature 1')),
        SimpleTerm(2, '2', _(u'Signature 2')),
        SimpleTerm(3, '3', _(u'Signature 3'))))
