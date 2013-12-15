# setup.py

# Copyright (c) 2012-2013 Harry van der Wolf. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.

# This file is part of pyexiftoolgui.
# pyexiftoolgui is a pySide script program that reads and writes  
# gps tags from/to files. It can use a "reference" image to write the
# gps tags to a multiple set of files that are taken at the same
# location.
# pyexiftoolgui is a graphical frontend for the open source
# command line tool exiftool by Phil Harvey, but it's not
# a complete exiftool gui: not at all.

from distutils.core import setup

os_files = [
	 # XDG application description
	 ('share/applications', ['xdg/pyexiftoolgui.desktop']),
	 # XDG application icon
	 ('share/pixmaps', ['logo/pyexiftoolgui.png']),
]


# main distutils setup (command)
dist = setup(name = "pyexiftoolgui",
        version = "0.4.0.2",
        description = "pyExifToolGui is a graphical frontend for ExifTool",
        author = "Harry van der Wolf",
        author_email = "hvdwolf@gmail.com",
        url = "http://hvdwolf.github.io/pyExifToolGUI",
        scripts     = ['bin/pyexiftoolgui'],
        packages    = ['scripts', 'scripts.ui', 'manual', 'logo', 'xdg'],
        package_data = { 
                       'scripts': ['*.py'],
                       'scripts.ui': ['*.py', '*.ui'], 
                       'manual' : ['*'], 
                       'logo' : ['*'], 
                       'xdg' : ['*'],
                       },
        data_files = os_files
    )

