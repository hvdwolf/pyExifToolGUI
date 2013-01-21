#!/usr/bin/env python

# setup.py

# Copyright (c) 2012 Harry van der Wolf. All rights reserved.
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

import os, sys, platform
from distutils.core import setup


#-- Functionality when script is used as distutils setup script
# Boolean: running as root?
ROOT = os.geteuid() == 0
# For Debian packaging it could be a fakeroot so reset flag to prevent execution of
# system update services for Mime and Desktop registrations.
# The debian/openshot.postinst script must do those.
if not os.getenv("FAKEROOTKEY") == None:
	print "NOTICE: Detected execution in a FakeRoot so disabling calls to system update services."
	ROOT = False

os_files = [
	 # XDG application description
	 ('share/applications', ['xdg/pyexiftoolgui.desktop']),
	 # XDG application icon
	 ('share/pixmaps', ['logo/pyexiftoolgui.png']),
]


UPD_FAILED = 'Tried to upgrade but it failed.\n\n'

# main distutils setup (command)
dist = setup(
        scripts     = ['bin/pyexiftoolgui'],
        packages    = ['scripts', 'scripts.ui'],
        package_data = { 'scripts.ui': ['*.ui'], 'manual' : ['*'], 'logo' : ['*'], 'xdg' : ['*'],
                       },
        data_files = os_files
    )

if ROOT and dist != None:
# update the XDG .desktop file database
    try:
        sys.stdout.write('Updating the .desktop file database.\n')
        subprocess.call(["update-desktop-database"])
    except:
        sys.stderr.write(UPD_FAILED)
        sys.stdout.write("\n-----------------------------------------------")
        sys.stdout.write("\nInstallation Finished!")
        sys.stdout.write("\nRun pyExifToolGUI by typing 'pyexiftoolgui' or ")
        sys.stdout.write("Run it through the Ubuntu Dash by starting to type pyexiftoolgui or ")
        sys.stdout.write("Run it via the Applications menu.")
        sys.stdout.write("\n-----------------------------------------------\n")
