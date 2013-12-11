# Copyright 2008-2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

from zope.interface import Interface

class ITags(Interface):
    """handler for the feeds tags.
    """
    
    def __call__():
        """list of tags.
        """
        
class ILogo(Interface):
    """handler for the logo for the feed.
    """
    
    def __call__():
        """absolute url to the logo image.
        """
    