# Copyright 2008-2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

from zope.interface import implements
from zope.component import adapts
from interfaces import ITags
from Products.Archetypes.interfaces import IBaseObject

class SubjectTagHandler(object):
    
    implements(ITags)
    adapts(IBaseObject)
    
    def __init__(self, context):
        self.context = context    
    
    def __call__(self):
        return self.context.Subject()