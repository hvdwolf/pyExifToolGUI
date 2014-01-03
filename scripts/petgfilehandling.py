# -*- coding: utf-8 -*-

# petgfilehandling.py - This python "helper" script holds file handling functions

# Copyright (c) 2012-2014 Harry van der Wolf. All rights reserved.
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

##################################################################################################
# Configuration xml file
def write_default_config():
    config = "<preferences>\n"
    config += "\t<alternate_exiftool>False</alternate_exiftool>\n"
    config += "\t<exiftooloption></exiftooloption>\n"
    config += "\t<pref_thumbnail_preview>True</pref_thumbnail_preview>\n"
    config += "\t<def_startupfolder></def_startupfolder>\n"
    config += "\t<def_creator></def_creator>\n"
    config += "\t<def_copyright></def_copyright>\n"
    config += "</preferences>\n"

    userpath = os.path.expanduser('~')
    config_file = open(os.path.join(userpath, '.pyexiftoolgui', 'config.xml'), "w")
    config_file.write(config)
    config_file.close()

def error_reading_configparameter(self):
    message = ("Somehow I encountered an error reading the config file.\n"
           "This can happen when:\n- you updated from version <= 0.5 to version >= 0.6\n"
           "- when the config file somehow got damaged.\n"
                   "- when this is the very first program start.\n\n"
           "I will simply create a new config file. Please "
           "check your preferences.")
    ret = QMessageBox.warning(self, "error reading config", message) 

def read_xml_config(self):
    tempstr = lambda val: '' if val is None else val

    userpath = os.path.expanduser('~')
    #print(userpath)
    print("reading from " + os.path.join(userpath, '.pyexiftoolgui', 'config.xml'))
    # First we check in the safe way for the existence of the config file
    if os.path.isfile(os.path.join(userpath, '.pyexiftoolgui', 'config.xml')):
        try:
            self.configtree = ET.parse(os.path.join(userpath, '.pyexiftoolgui', 'config.xml'))
            self.configroot = self.configtree.getroot()
        except:
            QMessageBox.critical(self, "Error!", "config.xml exists, but unable to open config.xml" )
            file_read = False
    else: # No lensdb.xml => first time use or whatever error
        error_reading_configparameter(self)
        write_default_config()
        self.configtree = ET.parse(os.path.join(userpath, '.pyexiftoolgui', 'config.xml'))
        self.configroot = self.configtree.getroot()

    for pref_record in self.configroot:
         for tags in pref_record.iter('alternate_exiftool'):
             if tags.text == "True":
               self.alternate_exiftool = True
             else:
               self.alternate_exiftool = False
         for tags in pref_record.iter('exiftooloption'):
               self.exiftooloption.setText(tags.text)
         for tags in pref_record.iter('pref_thumbnail_preview'):
             if tags.text == "True": 
               self.pref_thumbnail_preview.setChecked(1) 
             else:
               self.pref_thumbnail_preview.setChecked(0)
         for tags in pref_record.iter('def_startupfolder'):
               self.LineEdit_def_startupfolder.setText(tags.text)
         for tags in pref_record.iter('def_creator'):
               self.def_creator.setText(tags.text)
         for tags in pref_record.iter('def_copyright'):
               self.def_copyright.setText(tags.text)

def write_xml_config(self):
    for pref_record in self.configroot:
         for tags in pref_record.iter('alternate_exiftool'):
             if self.exiftooloption.text() == "":
               tags.text = "False"
               self.alternate_exiftool = False
             else:
               tags.text = "True"
               self.alternate_exiftool = True
         for tags in pref_record.iter('exiftooloption'):
             tags.text = self.exiftooloption.text()
         for tags in pref_record.iter('pref_thumbnail_preview'):
             if self.pref_thumbnail_preview.isChecked(): 
               tags.text = "True"
             else:
               tags.text = "False"
         for tags in pref_record.iter('def_startupfolder'):
             tags.text = self.LineEdit_def_startupfolder.text()
         for tags in pref_record.iter('def_creator'):
             tags.text = self.def_creator.text()
         for tags in pref_record.iter('def_copyright'):
             tags.text = self.def_copyright.text()

    try:
         userpath = os.path.expanduser('~')
         #print(userpath)
         self.configtree.write(os.path.join(userpath, '.pyexiftoolgui', 'config.xml'))
    except:
            QMessageBox.critical(self, "Error!", "Unable to open config.xml for writing" )


# End of Configuration xml file
##################################################################################################
# Lens config xml file
def write_default_lensdb():
    # If no lensdb exists, simply write a default lensdb to the users .pyexiftoolgui folder
    lensdb = "<data>\n"
    lensdb += "\t<lens name=\"Example: Panasonic Leica DG Summilux 25/f1.4\">\n"
    lensdb += "\t\t<make>Panasonic</make>\n"
    lensdb += "\t\t<model>Leica DG Summilux 25/f1.4</model>\n"
    lensdb += "\t\t<serialnumber>123456-ABC</serialnumber>\n"
    lensdb += "\t\t<focallength>25</focallength>\n"
    lensdb += "\t\t<focallengthin35mmformat>50</focallengthin35mmformat>\n"
    lensdb += "\t\t<fnumber>1.4</fnumber>\n"
    lensdb += "\t\t<maxaperturevalue />\n"
    lensdb += "\t</lens>\n"
    lensdb += "</data>\n"

    userpath = os.path.expanduser('~')
    lensdb_file = open(os.path.join(userpath, '.pyexiftoolgui', 'lensdb.xml'), "w")
    lensdb_file.write(lensdb)
    lensdb_file.close()

def read_defined_lenses(self, qApp):
    file_read = True
    tempstr = lambda val: '' if val is None else val

    userpath = os.path.expanduser('~')
    #print(userpath)
    print("reading from " + os.path.join(userpath, '.pyexiftoolgui', 'lensdb.xml'))
    # First we check in the safe way for the existence of the lensdb xml
    if os.path.isfile(os.path.join(userpath, '.pyexiftoolgui', 'lensdb.xml')):
        try:
            self.lensdbtree = ET.parse(os.path.join(userpath, '.pyexiftoolgui', 'lensdb.xml'))
            self.lensdbroot = self.lensdbtree.getroot()
        except:
            QMessageBox.critical(self, "Error!", "lensdb exists, but unable to open lensdb" )
            file_read = False
    else: # No lensdb.xml => first time use or whatever error
        write_default_lensdb()
        self.lensdbtree = ET.parse(os.path.join(userpath, '.pyexiftoolgui', 'lensdb.xml'))
        self.lensdbroot = self.lensdbtree.getroot()

    if file_read:
         self.loaded_lenses = ['none',]
         for lens in self.lensdbroot:
             self.loaded_lenses.append(lens.attrib["name"])
         self.predefined_lenses.clear()
         self.predefined_lenses.addItems(self.loaded_lenses)
    if self.lens_current_index <> '':
         self.predefined_lenses.setCurrentIndex(int(self.lens_current_index))


def write_lensdb_xml(self, qApp):
    try:
         userpath = os.path.expanduser('~')
         print(userpath)
         self.lensdbtree.write(os.path.join(userpath, '.pyexiftoolgui', 'lensdb.xml'))
    except:
            QMessageBox.critical(self, "Error!", "Unable to open lensdb for writing" )


def deletelens(self, qApp):
    print('delete lens data for this lens inside the lens database')
    self.lens_current_index = 0
    for lens in self.lensdbroot:
        if lens.attrib["name"]  == self.predefined_lenses.currentText():
           self.lensdbroot.remove(lens)

    write_lensdb_xml(self, qApp)
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

    self.lensdbroot.append(new_lens)
    rootstring = ET.tostring(self.lensdbroot)
    rootstring = rootstring.replace("</lens><lens ","</lens>\n\t<lens ")
    rootstring = rootstring.replace("</lens></data>","</lens>\n</data>")
    print(rootstring)
    self.lensdbroot = ET.fromstring(rootstring)

    write_lensdb_xml(self, qApp)
    read_defined_lenses(self, qApp)

##################################################################################################
# End of Lens config xml file

