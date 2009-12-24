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
""" Setup for zojax.forum package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='0'


setup(name = 'zojax.forum',
      version = version,
      author = 'Nikolay Kim',
      author_email = 'fafhrd91@gmail.com',
      description = "Forum for zojax.",
      long_description = (
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax'],
      install_requires = ['setuptools', 'ZODB3',
                          'zope.component',
                          'zope.interface',
                          'zope.schema',
                          'zope.i18n',
                          'zope.i18nmessageid',
                          'zope.security',
                          'zope.dublincore',
                          'zope.cachedescriptors',
                          'zope.lifecycleevent',
                          'zope.app.container',

                          'zojax.cache',
                          'zojax.mailin',
                          'zojax.content.type',
                          'zojax.content.forms',
                          'zojax.content.space',
                          'zojax.content.draft',
                          'zojax.content.feeds',
                          'zojax.content.attachment',
                          'zojax.content.notifications',
                          'zojax.principal.profile',
                          'zojax.catalog',
                          'zojax.product',
                          'zojax.richtext',
                          'zojax.filefield',
                          'zojax.ownership',
                          'zojax.table',
                          'zojax.layout',
                          'zojax.layoutform',
                          'zojax.resource',
                          'zojax.resourcepackage',
                          'zojax.statusmessage',
                          ],
      extras_require = dict(test=['zope.app.testing',
                                  'zope.app.zcmlfiles',
                                  'zope.app.zapi',
                                  'zope.testing',
                                  'zope.testbrowser',
                                  'zojax.security',
                                  'zojax.autoinclude',
                                  'zojax.personal.space',
                                  'zojax.personal.content',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
