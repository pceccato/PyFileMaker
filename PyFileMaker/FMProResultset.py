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

# Class defining the information about a resultset
class FMProResultset( FMProXML.FMProXML ):

    # Class constructor
    def __init__( self, data ):

        self.data = data
        
        self.errorcode = -1
        self.product = {}
        self.database = {}
        self.metadata = {}
        self.resultset = []
        self.fieldNames = []

        self.parseResultset()

    # Parse the resultset
    def parseResultset( self ):

        data = self.parseXMLData()

        self.errorcode = data.getElements( 'ERRORCODE' )[0].getData()

        node = self.getXMLElement( data, 'PRODUCT' )
        self.product = self.getXMLAttributes( node )

        node = self.getXMLElement( data, 'DATABASE' )
        self.database = self.getXMLAttributes( node )

        node = self.getXMLElement( data, 'METADATA' )
        for subnode in self.getXMLElements( node, 'FIELD' ):
            fieldData = self.getXMLAttributes( subnode )
            self.metadata[fieldData['NAME']] = fieldData
            self.fieldNames.append( fieldData['NAME'] )

        node = self.getXMLElement( data, 'RESULTSET' )
        for record in self.getXMLElements( node, 'ROW' ):

            recordData = []
            for column in self.getXMLElements( record, 'COL' ):
                try:
                    data = self.getXMLElement( column, 'DATA' )
                    recordData.append( data.getData() )
                except:
                    recordData.append( ''.encode( 'UTF-8' ) )

            recordDict = {}
            for i in range( len( recordData ) ):
                recordDict[ self.fieldNames[i] ] = recordData[i]

            recordDict['RECORDID'] = int(
                self.getXMLAttribute( record, 'RECORDID' )
            )

            recordDict['MODID'] = int(
                self.getXMLAttribute( record, 'MODID' )
            )

            self.resultset.append( recordDict )

    # Shows the contents of our resultset
    def show( self ):
        print 'Errorcode:', self.errorcode
        print 
        print 'Product information:'
        for key in self.product.keys():
            print '  ', key.encode( 'UTF-8' ),
            print '->', self.product[key].encode( 'UTF-8' )
        print
        print 'Database information:'
        for key in self.database.keys():
            print '  ', key.encode( 'UTF-8' ),
            print'->', self.database[key].encode( 'UTF-8' )
        print
        print 'Metadata:'
        for field in self.metadata.keys():
            print
            print '   ', field.encode( 'UTF-8' )
            for property in self.metadata[field]:
                print '       ', property.encode( 'UTF-8' ),
                print '->', self.metadata[field][property].encode( 'UTF-8') 
        print
        print 'Records:'
        for record in self.resultset:
            print
            for column in record:
                print '   ', column.encode( 'UTF-8' ),
                if type( record[column] ) == UnicodeType:
                    print '->', record[column].encode( 'UTF-8' )
                else:
                    print '->', record[column]

    # Show only the records
    def showRecords( self ):
        if len( self.resultset ) == 0:
            print 'No records found'
            return
        for record in self.resultset:
            print '-' * 80
            for column in record:
                print column.encode( 'UTF-8' ),
                if type( record[column] ) == UnicodeType:
                    print '->', record[column].encode( 'UTF-8' )
                else:
                    print '->', record[column]
        print '-' * 80
