# PyFileMaker 2.0 - Integrating FileMaker and Python 
# (c) 2002-2003 Pieter Claerhout, pieter@yellowduck.be
# 
# http://www.yellowduck.be/filemaker/

# Import the main modules
import string
from types import *

# Import the FMPro modules
import xml2obj
import FMProXML
from FMProError import *

# Class defining the information about a layout
class FMProLayout( FMProXML.FMProXML ):

    # Class constructor
    def __init__( self, data ):

        self.data = data
        
        self.errorcode = -1
        self.product = {}
        self.name = ''
        self.database = ''
        self.fields = {}
        self.valueLists = {}

        self.doParseResultset()

    # Parse the resultset
    def doParseResultset( self ):

        data = self.doParseXMLData()

        self.errorcode = data.getElements( 'ERRORCODE' )[0].getData()

        node = self.doGetXMLElement( data, 'PRODUCT' )
        self.product = self.doGetXMLAttributes( node )

        node = self.doGetXMLElement( data, 'LAYOUT' )
        self.database = self.doGetXMLAttribute( node, 'DATABASE' )
        self.name = self.doGetXMLAttribute( node, 'NAME' )

        for field in self.doGetXMLElements( node, 'FIELD' ):
            fieldData = {}
            for style in self.doGetXMLElements( field, 'STYLE' ):
                for attrib in self.doGetXMLAttributes( style ):
                    fieldData[attrib] = self.doGetXMLAttribute( style, attrib )
            self.fields[self.doGetXMLAttribute( field, 'NAME' )] = fieldData

        node = self.doGetXMLElement( data, 'VALUELISTS' )
        for valueList in self.doGetXMLElements( node, 'VALUELIST' ):
            valueListData = []
            for value in self.doGetXMLElements( valueList, 'VALUE' ):
                valueListData.append(
                    value.getData().encode( 'UTF-8' )
                )
            name = self.doGetXMLAttribute( valueList, 'NAME' )
            self.valueLists[ name ] = valueListData

    # Shows the contents of our resultset
    def show( self ):
        print 'Errorcode:', self.errorcode
        print 
        print 'Product information:'
        for key in self.product.keys():
            print '  ', key.encode( 'UTF-8' ),
            print '->', self.product[key].encode( 'UTF-8' )
        print
        print 'Layout information:'
        print
        print '   Name ->', self.name
        print '   Database ->', self.database
        print
        print 'Field information:'
        for field in self.fields.keys():
            print
            print '   ', field
            for attrib in self.fields[field].keys():
                print '       ', attrib.encode( 'UTF-8' ),
                print '->', self.fields[field][attrib]
        print
        print 'Value list information:'
        for valueList in self.valueLists.keys():
            print
            print '   ', valueList
            for value in self.valueLists[valueList]:
                print '       ', value.encode( 'UTF-8' )
