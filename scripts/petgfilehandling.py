# -*- coding: utf-8 -*-

# petgfilehandling.py - This python "helper" script holds file handling functions

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

import os, sys, platform, shlex, subprocess, time, re, string, datetime
import xml.etree.ElementTree as ET

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

def read_defined_lenses(self, qApp):
    try:
         if self.OSplatform == "Windows":
            if os.path.isfile(os.path.join(self.realfile_dir, "lensdb","lensdb.xml")): # from python executable
             tree = ET.parse(os.path.join(self.realfile_dir, "lensdb","lensdb.xml"))
            elif os.path.isfile(os.path.join(self.parent_dir, "lensdb","lensdb.xml")): # Started from script
             tree = ET.parse(os.path.join(self.parent_dir, "lensdb","lensdb.xml"))
         elif self.OSplatform == "Darwin":
            if os.path.isfile(os.path.join(self.realfile_dir, "pyexiftoolgui.app","Contents","MacOS","lensdb","lensdb.xml")): # from python app
             tree = ET.parse(os.path.join(self.realfile_dir, "pyexiftoolgui.app","Contents","MacOS","lensdb","lensdb.xml"))
            elif os.path.isfile(os.path.join(self.parent_dir, "lensdb","lensdb.xml")): # Started from script
             tree = ET.parse(os.path.join(self.parent_dir, "lensdb","lensdb.xml"))
         else:
            tree = ET.parse(os.path.join(self.realfile_dir, "lensdb","lensdb.xml"))
         root = tree.getroot()
         self.loaded_lenses = ['none',]
         for roottags in root.iter('lens'):
             self.loaded_lenses.append(roottags.get('name'))
             print('found lens: ' + roottags.get('name'))
         self.predefined_lenses.clear()
         self.predefined_lenses.addItems(self.loaded_lenses)
    except:
            QMessageBox.critical(self, "Error!", "Unable to open lensdb" )


