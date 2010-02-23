# PyFileMaker 2.0 - Integrating FileMaker and Python 
# (c) 2002-2003 Pieter Claerhout, pieter@yellowduck.be
# 
# http://www.yellowduck.be/filemaker/

# Import the main modules
import string
from types import *

# Import the FMPro modules
import xml2obj
from FMProError import *

# Class defining a basic FMPro XML result
class FMProXML:

    # This function parses the XML output of FileMaker
    def parseXMLData( self ):
        parser = xml2obj.Xml2Obj()
        xobj = parser.ParseString( self.data )
        self.errorcode = int( xobj.getElements( 'ERRORCODE' )[0].getData() )
        if self.errorcode != 0:
            FMProErrorByNum( self.errorcode )
        return xobj

    # Returns a specific element from the resultset
    def __getitem__( self, key ):
        return self.resultset[key]

    # Returns the length of the resultset. This is the same as the number of
    # records that were found
    def __len__( self ):
        return len( self.resultset )

    # Get a single element from a DOM element
    def getXMLElement( self, dom, elementName ):
        return dom.getElements( elementName )[0]

    # Get a list of elements from a DOM element
    def getXMLElements( self, dom, elementName ):
        return dom.getElements( elementName )

    # Get a list of elements from a DOM element
    def getXMLAttribute( self, dom, attribute ):
        return dom.getAttribute( attribute )

    # Get a list of attributes from a DOM element
    def getXMLAttributes( self, dom ):
        return dom.attributes

    # Shortcut for getting the XML
    def xml( self ):
        return self.data

    # Return the XML with a stylesheet applied to it
    def xmlWithXsl( self, xsl ):

        try:
            import Pyana
        except:
            raise FMProError( 'The Pyana library is not installed. You can download a copy from http://pyana.sourceforge.net.' )

        xsl = open( xsl, 'rb' )
        return str( Pyana.transform2String( self.data, xsl ) )

##        # We need libxml and libxsl loaded
##        try:
##            import libxml2
##            import libxslt
##        except:
##            raise FMProError( 'libxml and libxsl are not available.' )
##
##        # Parse the stylesheet
##        styleDoc = libxml2.parseFile( xsl )
##        style = libxslt.parseStylesheetDoc(styleDoc)
##
##        # Parse the document
##        doc = libxml2.parseDoc( self.data )
##
##        # Apply the stylesheet
##        result = style.applyStylesheet( doc, None )
##
##        # Get the result
##        res = style.saveResultToString( result )
##
##        # Free everything up
##        style.freeStylesheet()
##        doc.freeDoc()
##        result.freeDoc()
##
##        # Return the result
##        return res

    # Return the XML with a stylesheet applied to it and also save it
    def xmlWithXslToFile( self, xsl, file ):
        data = self.xmlWithXsl( xsl )
        f = open( file, 'wb' )
        f.write( data )
        f.close()
