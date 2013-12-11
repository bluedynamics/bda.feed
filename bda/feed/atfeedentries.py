# Copyright 2008-2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

from zope.interface import implements
from zope.component import adapts
from zope.component import queryAdapter
from zope.component import getMultiAdapter
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces import IReferenceable
from Products.Archetypes.ExtensibleMetadata import FLOOR_DATE
from Products.ATContentTypes.interface import IATDocument
from cornerstone.feed.core.interfaces import IFeedEntry
from cornerstone.feed.core.interfaces import IEnclosure
from interfaces import ITags

class ArchetypesFeedEntry(object):
    """Abstract common content adapter.
    """
    implements(IFeedEntry)
    
    def __init__(self, context):
        self.context = context
    
    @property 
    def contents(self):
        raise NotImplementedError(u"Abstract ArchetypesFeedEntry does not "
                                  u"implement ``contents``")
    
    @property
    def title(self):
        return self.context.Title()
    
    @property
    def description(self):
        return self.context.Description()
    
    @property
    def webURL(self):
        return self.context.absolute_url()
    
    @property
    def uid(self):
        return self.context.UID()
    
    @property
    def author(self):
        creator = self.context.Creator()
        member = self.context.portal_membership.getMemberById(creator)
        return member and member.getProperty('fullname') or creator
    
    @property
    def effectiveDate(self):
        effective = self.context.effective()
        if effective == FLOOR_DATE:
            effective = self.context.created()
        return effective
    
    @property
    def modifiedDate(self):
        return self.context.modified()
    
    @property
    def tags(self):
        taghandler = ITags(self.context)
        return taghandler()    
    
    @property
    def rights(self):
        return self.context.Rights()
    
    @property
    def enclosures(self):
        enclosurehandler = queryAdapter(self.context, IEnclosure)
        if enclosurehandler and len(enclosurehandler) > 0:
            return [enclosurehandler]


class ATBodyFeedEntry(ArchetypesFeedEntry):
    """Returns the rendered body of most types.
    """
    adapts(IReferenceable)

    @property 
    def contents(self):
        """The (x)html body content of this entry, or None
        
        @return: List of dicts with keys: body, mimetype, src(url).
        """
        body = self.context.feedproxy()
        body = body.replace('&nbsp;','&#xa0;')
        body = body.replace('&mdash;', '')
        res = [{'body': body,
                'type': 'xhtml',
                'src': '%s/feedproxy' % self.webURL}]
        return res

class ATDocumentFeedEntry(ArchetypesFeedEntry):
    """ATDocument adapter."""
    adapts(IATDocument)

    @property 
    def contents(self):
        """The (x)html body content of this entry, or None
        
        @return: List of dicts with keys: body, mimetype, src(url).
        """        
        res = [{'body': self.context.getText(contenttype="text/xhtml-safe", 
                        encoding='utf-8'),
                'type': 'xhtml',
                'src': '%s/view' % self.webURL}]
        return res

class ATPrimaryFieldEnclosure(object):
    implements(IEnclosure)
    adapts(IBaseObject)
    
    def __init__(self, context):
        self.context = context
       
    @property
    def url(self):
        if self._field:
           return '%s/at_download/%s' % (self.context.absolute_url(), 
                                         self._field.getName())           
    def getURL(self):
        """asomething
        """
        return self.url

    @property
    def major(self):
       type = self.getType()
       if type:
           return type.split('/')[0]

    @property
    def minor(self):
       type = self.getType()
       if type:
           return type.split('/')[1]

    @property
    def mimetype(self):
       if self._field:
           return self._field.getContentType(self.context)

    def __len__(self):
       if self._field:
           return self._field.get_size(self.context)
       return 0
   
    @property
    def _field(self):
        pfield = self.context.getPrimaryField()
        if pfield:
            raw = pfield.getRaw(self.context)
            #if not raw.filename:
                #raw.filename = pfield.getName()
        if pfield and self.context.isBinary(pfield.getName()):
            return pfield

    def getLength(self):
        return len(self)

    def getType(self):
        return self.mimetype
