# Copyright 2008-2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

from zope.interface import implements
from zope.component import adapts
from interfaces import ILogo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IBaseObject

class BasePropsLogoHandler(object):
    
    implements(ILogo)
    adapts(IBaseObject)
    
    def __init__(self, context):
        self.context = context    
    
    def __call__(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        baseprops = self.context.base_properties
        logo = baseprops.logoName
        return "%s/%s" % (portal_url, logo)