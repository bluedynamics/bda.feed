import os
from setuptools import setup, find_packages
from xml.dom.minidom import parse, parseString

mdfile = os.path.join(os.path.dirname(__file__), 'bda', 'feed', 'profile', 
                      'metadata.xml')
metadata = parse(mdfile)
assert metadata.documentElement.tagName == "metadata"
shortdesc = metadata.getElementsByTagName("description")[0].childNodes[0].data
readme = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

setup(name='bda.feed',
      version='2.0b2',
      description=shortdesc.strip(),
      long_description=readme,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='web zope plone atom syndication feed',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url='http://svn.plone.org/svn/collective/bda.feed',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bda'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'bda.contentproxy',
          'cornerstone.feed.zope',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
