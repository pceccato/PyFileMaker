# PyFileMaker 2.0 - Integrating FileMaker and Python
(c) 2002 Pieter Claerhout, [pieter@yellowduck.be](mailto:pieter@yellowduck.be)

## What is PyFileMaker?

PyFileMaker is a set of Python modules that makes it easy to access and modify
data stored in a FileMaker Pro database. You can use it to qeury a FileMaker
database, but you can also use it to add data to a FileMaker Pro database, you
can even use it to delete records and execute FileMaker Pro scripts.

## Requirements

In order to use PyFileMaker, you will need to have the following software
installed on your computer:

- Python version 2.0 or higher
- The xml.parsers.expat Python module to parse XML data
- FileMaker Pro 6 with the WebCampanion and XML enabled

This module was tested on Windows NT4, Windows 2000 and Windows XP. We also
tested the module on MacOS 9 and MacOS X version 10.1.5 and version 10.2.

Linux and Unix type of operating systems should work without any problems.

## How to install PyFileMaker

There is nothing special to configure on PyFileMaker. Just make sure the
PyFileMaker directory, which contains the file FMPro.py file is somewhere in 
your Python path so that Python knows where to find the module.

## How to setup your database

Since the PyFileMaker module relies on the FileMaker Pro Web Companion, you need
to have it turned on before you can use it. I normally configure it as follows:

   1. Open your database in FileMaker Pro
   2. Go to File -> Sharing and make sure Web Companion is selected
   3. Click on OK

You also might want to check the settings of the Web Companion plugin so that
you know the connection parameters. I always use the standard port 591.

## Where can I find more info?

* About Python: [www.python.org](http://www.python.org)
* About FileMaker Pro: [www.filemaker.com](http://www.filemaker.com)
* About PyFileMaker: [www.yellowduck.be](http://www.yellowduck.be)

## Changelog

###Version 2.0
- Changed the API funcion names to be more generic
- Added the script function that automatically executes a script
- The imageSave function can now automatically add the extension based on the
  image type of the image data which is being saved.

###Version 1.2a3
- The clearDBParams and clearSortParams functions are now working
- When using the doImg function, it now resets the database parameters and
  the sort parameters before returning the result.

###Version 1.2a2
- Now preserves newlines in field values

###Version 1.2a1
- Add support for basic http authentication and password protected databases.
  The function setPassword can be used for this purpose.
- Fixed a bug where findall would only return 25 records.

###Version 1.1
- Improved support for Macintosh OS X
- Now supports images
- Speed improvements thanks to switching from urllib to httplib

