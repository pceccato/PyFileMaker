# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# We first find the record (we need the record ID)
db.addDBParam( 'NewsTitle', 'Een nieuwsitem van pyFileMaker', 'eq' )
db.addDBParam( 'NewsBody', 'Hello from pyFileMaker', 'eq' )
db.addDBParam( 'NewsUser', 'Pieter Claerhout', 'eq' )
result = db.find()

# We change the fields
db.addDBParam( 'NewsTitle', 'Mijn eerste aangepaste titel van pyFileMaker' )
db.addDBParam( 'RECORDID', result[0]['RECORDID'] )

# Perform the edit request
result = db.edit()

# We show the contents of the result
result.showRecords()
