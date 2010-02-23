# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# We first find the record (we need the record ID)
db.addDBParam( 'NewsTitle', 'Mijn eerste aangepaste titel van pyFileMaker' )
db.addDBParam( 'NewsBody', 'Hello from pyFileMaker', 'eq' )
db.addDBParam( 'NewsUser', 'Pieter Claerhout', 'eq' )
result = db.find()

# We change the fields
db.addDBParam( 'RECORDID', result[0]['RECORDID'] )

# Perform the delete request
result = db.delete()

# We show the contents of the result
result.showRecords()
