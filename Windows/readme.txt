Readme for the windows folder inside pyexiftoolgui.

To build a Windows self contained executable that will run on any Windows system we need to have all the python scripts, 
the gui elements, the QT and pyside libraries and plugins, and the python dlls.

Currently I use pyinstaller 2.1 for this (http://www.pyinstaller.org/).

- I create the pyinstaller spec file, "linking" all the required elements.
- This pyexiftoolgui.spec file I copy into a pyexiftoolgui subfolder inside the
  pyinstaller program folder.
- Make sure that the path to the python executable is in your PATH. You might
  require cygwin as well for a couple of supplementary tools.
- run the following command from the pyinstaller folder (without the double quotes): 
  "python pyinstaller.py pyexiftoolgui\pyexiftoolgui.spec"
- If the paths in your .spec file are correct, your pyexiftoolgui.exe including 
  all the necessary files and dll libraries will be built.
- Use the unix2dos utility to change the unix line endings to DOS line endings in the Changelog by
  using the command "unix2dos Changelog"

This file: version 0.1, 2013-12-06, H. van der Wolf

