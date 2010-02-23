# PyFileMaker 2.0 - Integrating FileMaker and Python 
# (c) 2002-2003 Pieter Claerhout, pieter@yellowduck.be
# 
# http://www.yellowduck.be/filemaker/

# Import the main modules
import os
import sys
import base64
import string
import urllib
import imghdr
import httplib
import StringIO
import urlparse
from types import *
from exceptions import StandardError

# Import the FMPro modules
import xml2obj
import FMProLayout
import FMProResultset
from FMProError import *

# The main class for communicating with FileMaker Pro
class FMPro:

    # Class constructor
    def __init__( self, url='http://localhost:591/FMPro' ):

        self.url = url
        self.maxRecords = 0
        self.skipRecords = 0
        self.format = '-fmp_xml'
        self.layout = ''
        self.lop = 'AND'
        self.password = ''

        self.dbParams = []
        self.sortParams = []

    # Select the database to use. You don't need to specify the file extension. 
    # PyFileMaker will do this automatically.
    def setDb( self, db ):
        self.db = db

    # Select the right layout from the database
    def setLayout( self, layout ):
        self.layout = layout

    # This is the maximum number of records that FileMaker will return at once
    def setMaxRecords( self, maxRecords ):
        self.maxRecords = maxRecords

    # This is the number of records that FileMaker will skip
    def setSkipRecords( self, skipRecords ):
        self.skipRecords = skipRecords

    # Sets the way the find fields should be combined together.
    def setLogicalOperator( self, lop ):
        if not lop in ['AND', 'OR']:
            raise FMProError, 'Unsupported logical operator.'
        self.lop = lop

    # This is the password that will be used to access the database.
    def setPassword( self, password ):
        self.password = password

    # Adds a database parameter
    def addDBParam( self, name, value, oper='' ):
        if oper != '':
            validOperators = [
                'eq', 'equals',
                'cn', 'contains',
                'bw', 'begins with',
                'ew', 'ends with',
                'gt', 'greater than',
                'gte', 'greater than or equals',
                'lt', 'less than',
                'lte', 'less than or equals',
                'neq', 'not equals'
            ]
            if not string.lower( oper ) in validOperators:
                raise FMProError, 'Invalid operator for "' + field + '"'
        self.dbParams.append( [ name, value, string.lower( oper ) ] )

    # Adds a sort parameter
    def addSortParam( self, field, order='' ):
        if order != '':
            validSortOrders = [
                'ascend', 'ascending', 'descend', 'descending', 'custom'
            ]
            if not string.lower( order ) in validSortOrders:
                raise FMProError, 'Invalid sort order for "' + field + '"'
        self.sortParams.append( [ field, string.lower( order ) ] )

    # Resets the list of database parameters
    def clearDBParams():
        self.dbParams = []

    # Resets the list of sort parameters
    def clearSortParams():
        self.sortParams = []

    # This function returns the list of open databases
    def getDbNames( self ):

        request = []
        request.append( urllib.urlencode( {'-dbnames': '' } ) )

        result = self.doRequest( request )
        result = FMProResultset.FMProResultset( result )

        dbNames = []
        for dbName in result.resultset:
            dbNames.append( string.lower( dbName['DATABASE_NAME'] ) )
        
        return dbNames

    # This function returns the list of layouts for the current db
    def getLayoutNames( self ):

        if self.db == '':
            raise FMProError, 'No database was selected'

        request = []
        request.append( urllib.urlencode( {'-db': self.db } ) )
        request.append( urllib.urlencode( {'-layoutnames': '' } ) )

        result = self.doRequest( request )
        result = FMProResultset.FMProResultset( result )

        layoutNames = []
        for layoutName in result.resultset:
            layoutNames.append( string.lower( layoutName['LAYOUT_NAME'] ) )

        return layoutNames

    # This function returns the list of layouts for the current db
    def getScriptNames( self ):

        if self.db == '':
            raise FMProError, 'No database was selected'

        request = []
        request.append( urllib.urlencode( {'-db': self.db } ) )
        request.append( urllib.urlencode( {'-scriptnames': '' } ) )

        result = self.doRequest( request )
        result = FMProResultset.FMProResultset( result )

        scriptNames = []
        for scriptName in result.resultset:
            scriptNames.append( string.lower( scriptName['SCRIPT_NAME'] ) )

        return scriptNames

    # This function will check if a record ID was specified
    def checkRecordID( self ):
        hasRecID = 0
        for dbParam in self.dbParams:
            if dbParam[0] == 'RECORDID':
                hasRecID = 1
                break
        return hasRecID

    # This function will perform the command -find
    def find( self ):
        return self.action( '-find' )

    # This function will perform the command -findall
    def findAll( self ):
        return self.action( '-findall' )

    # This function will perform the command -findany
    def findAny( self ):
        return self.action( '-findany' )

    # This function will perform the command -delete
    def delete( self ):
        if self.checkRecordID() == 0:
            raise FMProError, 'RecordID is missing'
        return self.action( '-delete' )

    # This function will perform the command -edit
    def edit( self ):
        if len( self.dbParams ) == 0:
            raise FMProError, 'No data to be edited'
        if self.checkRecordID() == 0:
            raise FMProError, 'RecordID is missing'
        return self.action( '-edit' )

    # This function will perform the command -new
    def new( self ):
        if len( self.dbParams ) == 0:
            raise FMProError, 'No data to be added'
        return self.action( '-new' )

    # This function will perform the command -view
    def view( self ):
        if self.layout == '':
            raise FMProError, 'No layout was selected'
        return self.action( '-view' )

    # This function will perform the command -dbopen
    def dup( self ):
        if self.checkRecordID() == 0:
            raise FMProError, 'RecordID is missing'
        return self.action( '-dbopen' )

    # This function will perform the command -img
    def img( self ):

        request = []
        request.append( urllib.urlencode( {'-format': '' } ) )
        request.append( urllib.urlencode( {'-db': self.db } ) )
        for dbParam in self.dbParams:
            if dbParam[0] == 'RECORDID':
                request.append( urllib.urlencode( { '-recid': dbParam[1] } ) )
            else:
                request.append( urllib.urlencode( { dbParam[0]: dbParam[1] } ) )
        request.append( urllib.urlencode( {'-img': '' } ) )
        result = self.request( request )

        self.dbParams = []
        self.sortParams = []

        return result

    # This function will save the image to a file
    def imgSave( self, fName, autoExt=1 ):

        data = self.img()

        if autoExt == 1:
            imgType = imghdr.what( '', data )
            if imgType == 'jpeg' or imgType == None:
                imgType = 'jpg'
            fName = os.path.splitext( fName )[0] + '.' + imgType

        f = open( fName, 'wb' )
        f.write( data )
        f.close()

        self.dbParams = []
        self.sortParams = []

    # This will execute the indicated script
    def script( self, name ):
        self.addDBParam( '-script', name )
        return self.find()

    # This function will perform the command -dbopen
    def dbOpen( self, dbName ):

        request = []
        request.append( urllib.urlencode( {'-db': dbName } ) )
        request.append( urllib.urlencode( {'-dbopen': '' } ) )

        result = self.request( request )
        result = FMProResultset.FMProResultset( result )

        return result

    # This function will perform the command -dbclose
    def dbClose( self, dbName ):

        request = []
        request.append( urllib.urlencode( {'-db': dbName } ) )
        request.append( urllib.urlencode( {'-dbclose': '' } ) )

        result = self.request( request )
        result = FMProResultset.FMProResultset( result )

        return result

    # This function will perform a FileMaker action
    def action( self, action ):

        if self.db == '':
            raise FMProError, 'No database was selected'

        result = ""

        try:

            uu = urllib.urlencode

            request = []
            request.append( uu( {'-db': self.db } ) )

            if self.layout != '':
                request.append( uu( { '-layout': self.layout } ) )

            if action == '-find':
                request.append( uu( { '-lop': self.lop } ) )

            if action in ['-find', '-findall']:
                if self.skipRecords != 0:
                    request.append( uu( { '-skip': self.skipRecords } ) )
                if self.maxRecords != 0:
                    request.append( uu( { '-max': self.maxRecords } ) )
                else:
                    request.append( uu( { '-max': 'All' } ) )
                for sort in self.sortParams:
                    request.append( uu( { '-sortfield': sort[0] } ) )
                    if sort[1] != '':
                        request.append( uu( { '-sortorder': sort[1] } ) )

            for dbParam in self.dbParams:
                if dbParam[0] == 'RECORDID':
                    request.append( uu( { '-recid': dbParam[1] } ) )
                elif dbParam[0] == 'MODID':
                    request.append( uu( { '-modid': dbParam[1] } ) )
                else:
                    if action == '-find':
                        if ( dbParam[2] != '' ):
                            request.append( uu( { '-op': dbParam[2] } ) )
                    request.append( uu( { dbParam[0]: dbParam[1] } ) )

            request.append ( action )

            result = self.request( request )

            if action == '-view':
                result = FMProLayout.FMProLayout( result )
            else:
                result = FMProResultset.FMProResultset( result )

        finally:
            self.dbParams = []
            self.sortParams = []

        return result

    # This function will perform the specified request on the FileMaker server,
    # and it will return the raw result from FileMaker.
    def request( self, request ):

        uu = urllib.urlencode

        hasFormat = 0
        for requestitem in request:
            if requestitem.startswith( '-format' ):
                hasFormat = 1
                break
        
        if not hasFormat:
            request.insert(0, uu( {'-format': self.format } ) )

        request = '&'.join( request )
        
        if '--debug' in sys.argv:
            print self.url
            print request

        h = httplib.HTTP( urlparse.urlparse( self.url )[1] )
        h.putrequest( 'GET', '/FMPro?' + request )
        h.putheader( 'User-agent', 'PyFileMaker 2.0' )
        h.putheader('Accept', 'text/html')
        h.putheader('Accept', 'text/plain')

        if self.password != '':
            auth = base64.encodestring( 'pyfilemaker:' + self.password )
            auth = string.join( string.split( auth ), '' )
            h.putheader( 'Authorization', 'Basic ' + auth )

        h.endheaders()
        h.getreply()
        f = h.getfile()
        
        try:
            data = f.read()
        except:
            data = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
            <FMPXMLRESULT xmlns=\"http://www.filemaker.com/fmpxmlresult\">
                <ERRORCODE>0</ERRORCODE>
                <PRODUCT BUILD=\"5/4/2002\" NAME=\"FileMaker Pro Web Companion\" VERSION=\"6.0v1\"/>
                <DATABASE DATEFORMAT=\"\" LAYOUT=\"\" NAME=\"%s\" RECORDS=\"0\" TIMEFORMAT=\"\"/>
                <METADATA></METADATA>
                <RESULTSET FOUND=\"0\"></RESULTSET>
            </FMPXMLRESULT>""" %( self.db )
            
        f.close()

        return data
