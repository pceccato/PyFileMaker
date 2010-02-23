# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# Now we select the right layout
db.setLayout( 'Detail' )

# We get the details of the layout
result = db.view()

# We show the contents of the result
result.show()
