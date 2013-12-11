# Copyright 2008-2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

from datetime import datetime 
from zope.interface import implements
from Acquisition import Explicit
from Products.Archetypes.ExtensibleMetadata import FLOOR_DATE
from Products.CMFCore.utils import getToolByName
from cornerstone.feed.core.interfaces import IFeed
from cornerstone.feed.core.interfaces import IFeedEntryFactory
from interfaces import ILogo

class FeedMixin(object):
    """A base mixin class for IFeed implementations.
    
    Doesn't depend on a specific interface supplied by context, but expects
    Dublin-Core accessors, so should be generically useful.
    
    not implemented by this mixin:
    * max
    * factories
    """  
    
    @property
    def uid(self):
        return self.context.UID()
    
    @property
    def feedURL(self):
        return self.webURL + '/++feed++/atom.xml' # XXX    
    
    @property
    def baseURL(self):
        return getToolByName(self.context, 'portal_url')()    
    
    @property
    def imageURL(self):
        logo = ILogo(self.context)        
        return logo()
    
    iconURL = imageURL
    
    @property
    def webURL(self):
        return self.context.absolute_url()

    @property
    def title(self):
        return self.context.Title()  

    @property
    def description(self):
        return self.context.Description()    
    
    @property
    def author(self):
        """Author of this entry."""
        creator = self.context.Creator()
        member = self.context.portal_membership.getMemberById(creator)
        author = member and member.getProperty('fullname') or creator
        if author:
            return author
        return None    

    @property
    def rights(self):
        return self.context.Rights() 
        
    @property
    def encoding(self):
        pp = getToolByName(self, 'portal_properties')
        return pp.site_properties.getProperty('default_charset')    
    
    @property
    def generator(self):
        return dict(text="bda.feed by courtesy of BlueDynamics Alliance",
                    uri="http://bluedynamics.com" ,
                    version='2')
    
    @property
    def modifiedDate(self):
        entries = self.getFeedEntries()
        if not entries:
            return datetime.now()
        modified = entries[0].modifiedDate
        for feedentry in entries[1:]:
            if feedentry.modifiedDate > modified:
                modified = feedentry.modifiedDate
        return modified
        
    @property
    def updatePeriod(self):
        syntool = getToolByName(self, 'portal_syndication')
        return syntool.getUpdatePeriod()
        
    @property
    def updateFrequency(self):
        syntool = getToolByName(self, 'portal_syndication')
        return syntool.getUpdateFrequency()

    def getFeedEntries(self, limit=True):
        """Sorted sequence of IFeedEntry objects with which to build a feed.

        Sorting based on publication datetime, newest first.
        
        @param limit: limit to 'max' entries
        """           
        entries = []
        for factory in self.factories:
            entries.extend(list(factory))
        entries.sort(
            lambda x, y: cmp(y.effectiveDate, x.effectiveDate)
        )
        if limit and self.max:
            entries = entries[:self.max]
        return entries
    
class FeedWithSingleSource(FeedMixin, Explicit):
    """Feed with single feed source on context expected.
    """
    implements(IFeed)

    def __init__(self, context):
        self.context = context
        self._factory = None      

    @property
    def factories(self):
        if self._factory is None:
            self._factory = IFeedEntryFactory(self.context)        
        return [self._factory,]
    
    @property
    def max(self):
        return 0 # XXX