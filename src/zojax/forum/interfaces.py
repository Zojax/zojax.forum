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
""" zojax.forum interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.forum')

from zojax.forum import vocabulary
from zojax.richtext.field import RichText
from zojax.filefield.field import ImageField
from zojax.security.interfaces import IPermissionCategory
from zojax.content.type.interfaces import IItem
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory
from zojax.content.notifications.interfaces import IContentNotification

TOPIC_FIRST_MESSAGE = '00000'


class IForumContentType(interface.Interface):
    """ 'Forum' content type """


class ITopicContentType(interface.Interface):
    """ 'Topic' content type """


class IForumFolder(IItem):
    """ container for forums """

    icon = ImageField(
        title = _(u'Icon'),
        description = _('Upload forum icon.'),
        required = False)


class IForumFolderType(interface.Interface):
    """ forum folder content type """


class IForum(interface.Interface):
    """ container for forum topics """

    topics = interface.Attribute('Sorted topics.')

    count_topics = interface.Attribute('Number of topics in forum.')

    count_replies = interface.Attribute('Number of replies in forum.')

    lastTopic = interface.Attribute('Last topic')

    firstTopic = interface.Attribute('First topic')

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Forum title.'),
        required=True)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'Forum description.'),
        default = u'',
        required=False)

    icon = ImageField(
        title = _(u'Icon'),
        description = _('Upload forum icon.'),
        required = False)

    text = RichText(
        title = _(u'Forum text'),
        required = False)


class IForumType(interface.Interface):
    """ forum content type """


class ITopic(IItem):
    """ forum topic """

    messages = interface.Attribute('Messages (Sorted)')

    lastMessage = interface.Attribute('Last message')


class ITopicType(interface.Interface):
    """ topic content type """


class ITopics(interface.Interface):
    """ forum topics """

    topics = interface.Attribute('Topics')

    def __getitem__(idx):
        """ get topic by it number """

    def append(topic):
        """ append topic to list """

    def remove(topic):
        """ remove topic from list """

    def next(topic):
        """ return next topic """

    def previous(topic):
        """ return prev topic """


class IMessage(interface.Interface):
    """ topic message """

    title = schema.TextLine(
        title = _(u'Title'),
        default = u'',
        required=False)

    text = RichText(
        title = _(u'Message text'),
        required = True)

    signature = schema.Choice(
        title = _(u'Signature'),
        description = _(u'Signatures are displayed at the bottom of '
                        u'each post or personal message.'),
        default = 1,
        vocabulary = vocabulary.Signatures,
        required = False)


class IFirstMessage(interface.Interface):
    """ first message in topic """


class IMessageType(interface.Interface):
    """ forum content type """


class IIdGenerator(interface.Interface):
    """ id generator, format '00000' """

    nextId = interface.Attribute(u'Next id')


class IForumPreferences(interface.Interface):
    """ forum preferences """


class ISignatures(interface.Interface):
    """ principal message signatures """

    signature1 = schema.Text(
        title = _(u'Signature 1'),
        description = _(u'Message signature.'),
        default = u'',
        required = False)

    signature2 = schema.Text(
        title = _(u'Signature 2'),
        description = _(u'Message signature.'),
        default = u'',
        required = False)

    signature3 = schema.Text(
        title = _(u'Signature 3'),
        description = _(u'Message signature.'),
        default = u'',
        required = False)

    default = schema.Choice(
        title = _(u'Default signature'),
        description = _(u'Select signatures that '
                        u'will be used as default signature.'),
        default = 1,
        vocabulary = vocabulary.Signatures,
        required = False)


class IForumProduct(interface.Interface):
    """ forum product """

    forum_page_size = schema.Int(
        title = _('Number of topics on page.'),
        default = 20)

    topic_page_size = schema.Int(
        title = _('Number of messages on page.'),
        default = 20)


class IForumWorkspace(IForum, IWorkspace):
    """ forum workspace """


class IForumsWorkspace(IForumFolder, IWorkspace):
    """ forums workspace """


class IForumWorkspaceFactory(IWorkspaceFactory):
    """ forum workspace factory """


class IForumWorkspaceFactory(IWorkspaceFactory):
    """ forums workspace factory """


class IForumRSSFeed(interface.Interface):
    """ forum rss feed """


class IForumNotification(IContentNotification):
    """ forum notification """


class ITopicNotification(IContentNotification):
    """ topic notification """


class IForumPermissions(IPermissionCategory):
    """ forum permissions """
