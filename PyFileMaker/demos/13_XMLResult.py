# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# Perform the findall request
result = db.findAll()

# We show the contents of the result, but this time as XML
result.xml()
