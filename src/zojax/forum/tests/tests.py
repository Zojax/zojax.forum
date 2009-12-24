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
""" zojax.forum tests

$Id$
"""
import os, unittest, doctest
from zope import interface, component, event
from zope.component import eventtesting
from zope.app.testing import setup, functional
from zope.app.component.hooks import setSite
from zope.app.rotterdam import Rotterdam
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectCreatedEvent
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.catalog.catalog import Catalog
from zojax.catalog.interfaces import ICatalog
from zojax.content.space.content import ContentSpace
from zojax.personal.space.manager import PersonalSpaceManager, IPersonalSpaceManager
from zojax.content.type.testing import setUpContents

from zojax.forum import interfaces
from zojax.forum import topic, forum, message, idgenerator


zojaxForumLayer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxForumLayer', allow_teardown=True)


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


def FunctionalDocFileSuite(*paths, **kw):
    layer = zojaxForumLayer

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        root = functional.getRootFolder()
        setSite(root)
        sm = root.getSiteManager()

        # IIntIds
        root['ids'] = IntIds()
        sm.registerUtility(root['ids'], IIntIds)
        root['ids'].register(root)

        # catalog
        root['catalog'] = Catalog()
        sm.registerUtility(root['catalog'], ICatalog)

        # space
        space = ContentSpace(title=u'Space')
        event.notify(ObjectCreatedEvent(space))
        root['space'] = space

        # people
        people = PersonalSpaceManager(title=u'People')
        event.notify(ObjectCreatedEvent(people))
        root['people'] = people
        sm.registerUtility(root['people'], IPersonalSpaceManager)

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def setUp(test):
    setup.placefulSetUp()
    setUpContents()

    eventtesting.setUp()
    component.provideAdapter(idgenerator.NameChooser)

    component.provideHandler(topic.topicIdAddedHandler)
    component.provideHandler(topic.topicModifiedHandler)
    component.provideHandler(topic.topicRemovedHandler)
    component.provideHandler(message.messageModifiedHandler)


def tearDown(test):
    setup.placelessTearDown()


def test_suite():
    return unittest.TestSuite((
            doctest.DocFileSuite(
                'topics.txt',
                setUp=setUp, tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            doctest.DocFileSuite(
                'idgenerator.txt',
                setUp=setUp, tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            FunctionalDocFileSuite('testbrowser.txt'),
            FunctionalDocFileSuite('mailin.txt'),
            FunctionalDocFileSuite('ws.txt'),
            ))
