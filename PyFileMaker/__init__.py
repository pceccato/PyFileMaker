# PyFileMaker 2.0 - Integrating FileMaker and Python 
# (c) 2002-2004 Pieter Claerhout, pieter@yellowduck.be
# 
# http://www.yellowduck.be/filemaker/

# Import the main modules
import sys

# Try to import the expat library
try:
    from xml.parsers import expat
except:
    print "Unable to load the EXPAT library. You need to have it installed"
    print "before you can use pyFileMaker."
    sys.exit()

# Import the FMPro core
from FMPro import *
from FMProError import *

# Shortcut to a FileMaker Pro database
def FMProDb( db, host='localhost', port=591 ):
    url = 'http://%s:%s' %( host, port )
    fmpdb = FMPro( url )
    fmpdb.setDb( db )
    return fmpdb
