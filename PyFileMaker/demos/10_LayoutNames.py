# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# We show the names of the layouts for the selected database
print db.getLayoutNames()
