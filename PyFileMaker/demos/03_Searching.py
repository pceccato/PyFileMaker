# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# We only want to see the items from Pieter Claerhout that have a body 
db.addDBParam( 'NewsUser', 'Pieter Claerhout', 'eq' )
db.addDBParam( 'NewsBody', '', 'neq' )

# Perform the find request
result = db.find()

# We show the contents of the result
result.showRecords()
