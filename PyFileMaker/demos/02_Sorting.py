# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# Add the sorting parameter. We will sort on the NewsUser field
db.addSortParam( 'NewsUser', 'Ascend' )

# Perform the findall request
result = db.findAll()

# We show the contents of the result
result.showRecords()
