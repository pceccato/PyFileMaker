# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# We fill in the fields
db.addDBParam( 'NewsTitle', 'Een nieuwsitem van pyFileMaker' )
db.addDBParam( 'NewsBody', 'Hello from pyFileMaker' )
db.addDBParam( 'NewsUser', 'Pieter Claerhout' )

# Perform the new request
result = db.new()

# We show the contents of the result
result.showRecords()
