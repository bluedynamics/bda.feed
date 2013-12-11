# Copyright 2008-2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

from zope.interface import implements
from zope.component import adapts
from zope.component import queryAdapter
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATTopic
from cornerstone.feed.core.interfaces import IFeedEntryFactory
from cornerstone.feed.core.interfaces import IFeedEntry

class CollectionFeedEntryFactory(object):
    """A sequence of IFeedEntry objects from a collection.

    This means the actual objects, not catalog brains or so.
    """    
    adapts(IATTopic)    
    implements(IFeedEntryFactory)
    
    def __init__(self, context):
        self.context = context
        
    def __iter__(self):
        brains = self.context.queryCatalog()
        for brain in brains:
            # XXX expensive!
            obj = brain.getObject()
            entry = queryAdapter(obj, IFeedEntry)
            if entry is not None:
                yield entry

    