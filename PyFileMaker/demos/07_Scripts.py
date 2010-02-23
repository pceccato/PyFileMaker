# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# Execute the script
result = db.script( 'SearchScript' )

# We show the contents of the result
result.showRecords()
