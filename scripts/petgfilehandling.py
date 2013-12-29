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
    file_read = True
    tempstr = lambda val: '' if val is None else val

    try:
         if self.OSplatform == "Windows":
            if os.path.isfile(os.path.join(self.realfile_dir, "lensdb","lensdb.xml")): # from python executable
             self.tree = ET.parse(os.path.join(self.realfile_dir, "lensdb","lensdb.xml"))
            elif os.path.isfile(os.path.join(self.parent_dir, "lensdb","lensdb.xml")): # Started from script
             self.tree = ET.parse(os.path.join(self.parent_dir, "lensdb","lensdb.xml"))
         elif self.OSplatform == "Darwin":
            if os.path.isfile(os.path.join(self.realfile_dir, "pyexiftoolgui.app","Contents","MacOS","lensdb","lensdb.xml")): # from python app
             self.tree = ET.parse(os.path.join(self.realfile_dir, "pyexiftoolgui.app","Contents","MacOS","lensdb","lensdb.xml"))
            elif os.path.isfile(os.path.join(self.realfile_dir, "lensdb","lensdb.xml")): # Started from script
             self.tree = ET.parse(os.path.join(self.realfile_dir, "lensdb","lensdb.xml"))
         else:
            self.tree = ET.parse(os.path.join(self.realfile_dir, "lensdb","lensdb.xml"))
         self.root = self.tree.getroot()
    except:
            QMessageBox.critical(self, "Error!", "Unable to open lensdb" )
            file_read = False

    if file_read:
         self.loaded_lenses = ['none',]
         for lens in self.root:
             self.loaded_lenses.append(lens.attrib["name"])
         self.predefined_lenses.clear()
         self.predefined_lenses.addItems(self.loaded_lenses)
    if self.lens_current_index <> '':
         self.predefined_lenses.setCurrentIndex(int(self.lens_current_index))


def write_xml_file(self, qApp):
    try:
         if self.OSplatform == "Windows":
            if os.path.isfile(os.path.join(self.realfile_dir, "lensdb","lensdb.xml")): # from python executable
             self.tree.write(os.path.join(self.realfile_dir, "lensdb","lensdb.xml"))
            elif os.path.isfile(os.path.join(self.parent_dir, "lensdb","lensdb.xml")): # Started from script
             self.tree.write(os.path.join(self.parent_dir, "lensdb","lensdb.xml"))
         elif self.OSplatform == "Darwin":
            if os.path.isfile(os.path.join(self.realfile_dir, "pyexiftoolgui.app","Contents","MacOS","lensdb","lensdb.xml")): # from python app
             self.tree.write(os.path.join(self.realfile_dir, "pyexiftoolgui.app","Contents","MacOS","lensdb","lensdb.xml"))
            elif os.path.isfile(os.path.join(self.realfile_dir, "lensdb","lensdb.xml")): # Started from script
             self.tree.write(os.path.join(self.realfile_dir, "lensdb","lensdb.xml"))
         else:
            self.tree.write(os.path.join(self.realfile_dir, "lensdb","lensdb.xml"))
    except:
            QMessageBox.critical(self, "Error!", "Unable to open lensdb for writing" )


def deletelens(self, qApp):
    print('delete lens data for this lens inside the lens database')
    self.lens_current_index = 0
    for lens in self.root:
        if lens.attrib["name"]  == self.predefined_lenses.currentText():
           self.root.remove(lens)

    write_xml_file(self, qApp)
    read_defined_lenses(self, qApp)


def savelens(self, qApp):
# This function saves the lens data itself into the lens database
    print('save lens data itself into the lens database')
    new_lens = ET.Element('lens', name=self.lens_make.text() + ' ' + self.lens_model.text())
    lensnode = ET.Element('make')
    lensnode.text = self.lens_make.text()
    new_lens.append(lensnode)
    lensnode= ET.Element('model')
    lensnode.text = self.lens_model.text()
    new_lens.append(lensnode)
    lensnode= ET.Element('serialnumber')
    lensnode.text = self.lens_serialnumber.text()
    new_lens.append(lensnode)
    lensnode= ET.Element('focallength')
    lensnode.text = self.lens_focallength.text()
    new_lens.append(lensnode)
    lensnode= ET.Element('focallengthin35mmformat')
    lensnode.text = self.lens_focallengthin35mmformat.text()
    new_lens.append(lensnode)
    lensnode= ET.Element('fnumber')
    lensnode.text = self.lens_fnumber.text()
    new_lens.append(lensnode)
    lensnode= ET.Element('maxaperturevalue')
    lensnode.text = self.lens_maxaperturevalue.text()
    new_lens.append(lensnode)
    new_lens_string = ET.tostring(new_lens)
    new_lens_string = new_lens_string.replace("><",">\n\t\t<")
    new_lens = ET.fromstring(new_lens_string)

    self.root.append(new_lens)
    rootstring = ET.tostring(self.root)
    rootstring = rootstring.replace("</lens><lens ","</lens>\n\t<lens ")
    rootstring = rootstring.replace("</lens></data>","</lens>\n</data>")
    print(rootstring)
    self.root = ET.fromstring(rootstring)

    write_xml_file(self, qApp)
    read_defined_lenses(self, qApp)


