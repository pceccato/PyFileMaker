# Importing the PyFileMaker module
import PyFileMaker

# Making the connection.
db = PyFileMaker.FMProDb( 'SampleDB.fp5' )

# Add a database parameter
db.addDBParam( 'RECORDID', 2 )
db.addDBParam( 'NewsImage', '' )

# Perform the image request
data = db.img()

# Save it to a file
f = open( '08_Images.jpg', 'wb' )
f.write( data )
f.close()
