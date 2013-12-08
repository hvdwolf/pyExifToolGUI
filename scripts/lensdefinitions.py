# -*- coding: utf-8 -*-

# lensdefinitions.py - This python "helper" script holds the lensdefinition functions

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

import os, sys, platform, shlex, subprocess, re, string

import PySide
from PySide.QtCore import *
from PySide.QtGui import *
#from PySide.QtUiTools import *

import programstrings
import petgfunctions

from ui_lensdefinition import Ui_lensdefinitiondialog

#------------------------------------------------------------------------
#--- All functions to maintain and read lensinformation
class dialog_lensdefinition(QDialog, Ui_lensdefinitiondialog):
	# This loads the py file created by pyside-uic from the ui.
	# the Quiloader segfaults on windows after ending the function
	def __init__(self, parent=None):
		super(dialog_lensdefinition, self).__init__(parent)
		self.setupUi(self)
		# set proper events
		self.btn_qdldf_save.clicked.connect(self.save_lensdefinition)
		self.btn_qdldf_cancel.clicked.connect(self.cancel_lensdialog)
		self.btn_qdldf_select.clicked.connect(self.select_lensdefinition)
		print("open lensdefinition dialog to select, create or modify a lens definition")


	def cancel_lensdialog(self):
		print("You pressed the cancel button in the lensdialog")
		self.close()
		#self.statusbar.showMessage("You pressed the cancel button in the lensdialog")

	def select_lensdefinition(self):
		print("You pressed the select button in the lensdialog")
		self.close()
		#self.statusbar.showMessage("You pressed the select button in the lensdialog")

	def save_lensdefinition(self):
		print("You pressed the save button in the lensdialog")
		lensparameters = {}
		lensparameters['make'] = self.lens_make
		lensparameters['model'] = self.lens_model
		lensparameters['serialnumber'] = self.lens_serialnumber
		lensparameters['focallength'] = self.lens_focallength
		lensparameters['focallengthin35mmformat'] = self.lens_focallengthin35mmformat
		lensparameters['fnumber'] = self.lens_fnumber
		lensparameters['maxaperturevalue'] = self.lens_maxaperturevalue

		if self.checkBox_qdldf_new_lens.isChecked():
			action = "CreateLens"
		else:
			action = "ModifyLens"

		# Check if lensconfig already exists
		Checked = lensdefinitions.lensdefinition_dialog.read_lensconfig(self, "check")
		if Checked == "lensconfig_exists":
			lensdefinitions.lensdefinition_dialog.write_lensconfig(self, action, lensparameters)
		else:
			lensdefinitions.lensdefinition_dialog.write_lensconfig(self, "Create", lensparameters)
			lensdefinitions.lensdefinition_dialog.write_lensconfig(self, action, lensparameters)

		self.close
		#self.statusbar.showMessage("You pressed the save button in the lensdialog")

	def check_new_checkbox(self):
		if self.checkBox_qdldf_new_lens.isChecked():
			self.qdldf_selectlens_combobox.setEnabled(False)
			self.qdldf_selectlens_label.setEnabled(False)
		else:
			self.qdldf_selectlens_combobox.setEnabled(True)
			self.qdldf_selectlens_label.setEnabled(True)

#---
def process_lensdialog(self,qApp):
	self.statusbar.showMessage("Opened the lens definition dialog")
	self.lensdefinition_dialog = dialog_lensdefinition()
	# initialize checkbox event
	self.lensdefinition_dialog.checkBox_qdldf_new_lens.clicked.connect(self.lensdefinition_dialog.check_new_checkbox)
	ret = self.lensdefinition_dialog.exec_()


###################################################################################################################
# Reading writing our lens config
###################################################################################################################
def write_lensconfig(self, write_action, lensparameters):
    if sys.version_info>(3,0,0):
        print("We are on python 3")
        # for python3 we use it's own write_config3 function
        write_lensconfig3(self, write_action)
        return
        #import configparser
        #config = configparser.ConfigParser()
    elif sys.version_info<(2,7,0):
        sys.stderr.write("\n\nYou need python 2.7 or later to use pyexiftoolgui\n")
        exit(1) 
    else: # 2.7.0 < version < 3.0.0
        import ConfigParser
        config = ConfigParser.RawConfigParser()

    # Here we write to our pyexiftoolgui config file
    #print "Writing our config file"

    # Create our config
    if (write_action == "read_error"): # Some error occurred, go back to defaults. Or first ever read of the non-existent lensconfig.cfg
        config.add_section("Basis")
        config.set("Basis", "defined_lenses", "")
#        config.set("Basis", "Date", "")
    elif write_action == "Create": #Simply create the first lens
        config.add_section("Basis")
        config.set("Basis", "defined_lenses", "")
    elif write_action == "CreateLens": #Simply create the first lens
	print("Creating a new lens")
    elif write_action == "ModifyLens":
        print("Modifying an existing lens")

    userpath = os.path.expanduser('~')
    try:
        fldr = os.mkdir(os.path.join(userpath, '.pyexiftoolgui'))
        #print "fldr gives: " + fldr
    except:
        print("Check for config folder: exists => OK")
    try:
        with open(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg'), 'wb') as configfile:
            config.write(configfile)
            succes = 1
    except:
        print("couldn't write lens configfile")
        success = 0

    return success

def write_lensconfig3(self, aftererror, lensparameters):
    import configparser
    config = configparser.ConfigParser()

    # Here we write to our pyexiftoolgui lensconfig file
    #print "Writing our config file"

    # Create our config
    config["preferences"] = {}
    if aftererror == 1: # Some error occurred. Go back to defaults
        config["preferences"]["alternate_exiftool"] = str(False)
        self.alternate_exiftool = False
        config["preferences"]["exiftooloption"] = "exiftool"
        config["preferences"]["pref_thumbnail_preview"] = str(True)
        config["preferences"]["def_creator"] = ""
        config["preferences"]["def_copyright"] = ""
    else:
        if self.exiftooloption.text() in ("exiftool", ""):
            config["preferences"]["alternate_exiftool"] = str(False)
            config["preferences"]["exiftooloption"] = "exiftool"
        else: # user has changed it
            config["preferences"]["alternate_exiftool"] = str(True)
            config["preferences"]["exiftooloption"] = self.exiftooloption.text()
            if self.pref_thumbnail_preview.isChecked():
               config["preferences"]["pref_thumbnail_preview"] = str(True)
            else:
               config["preferences"]["pref_thumbnail_preview"] = str(False)
        config["preferences"]["def_creator"] = self.def_creator.text()
        config["preferences"]["def_copyright"] = self.def_copyright.text()

    userpath = os.path.expanduser('~')
    try:
        fldr = os.mkdir(os.path.join(userpath, '.pyexiftoolgui'))
        #print "fldr gives: " + fldr
    except:
        print("Check for config folder: exists => OK")
    try:
        with open(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg'), 'w') as configfile:
            config.write(configfile)
    except:
        print("couldn't write configfile")
# end of write_config3: The python3 config writer


def error_reading_configparameter(self):
    message = ("Somehow I encountered an error reading the config file.\n"
           "This can happen when:\n- an updated version added or removed a parameter\n"
           "- when the config file somehow got damaged.\n"
                   "- when this is the very first program start.\n\n"
           "I will simply create a new config file. Please "
           "check your lens definition(s).")
    ret = QMessageBox.warning(self, "error reading config", message) 
    # simply run the write_config function to create our initial config file
    write_lensconfig(self, "read_error")

def read_lensconfig(self, read_action):
    if sys.version_info>(3,0,0):
        print("We are on python 3. We will use the python3 read_config3 configparser")
        #import configparser
        #config = configparser.ConfigParser()
        read_lensconfig3(self, read_action)
        return
    elif sys.version_info<(2,7,0):
        sys.stderr.write("\n\nYou need python 2.7 or later to use pyexiftoolgui\n")
        exit(1) 
    else: # 2.7.0 < version < 3.0.0
        import ConfigParser
        config = ConfigParser.RawConfigParser()

    #print "Reading our config file"
    userpath = os.path.expanduser('~')
    print(userpath)
    print(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg'))
    # First we check in the safe way for the existence of the config file
    if os.path.isfile(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg')):
        try:
            with open(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg')) as f: pass
            # If no error we can continue
            #print "no error on config check"
            if read_action == "check":
               return "lensconfig_exists"
            print("reading lensconfig.cfg")
            config.read(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg'))
            #print("lensconfig.cfg read")
            try: 
                self.alternate_exiftool = config.getboolean("preferences", "alternate_exiftool")
            except:
                error_reading_configparameter(self)  
            try:
                self.exiftooloption.setText(config.get("preferences", "exiftooloption"))
            except:
                error_reading_configparameter(self)
            try:
                if config.get("preferences", "pref_thumbnail_preview") == "True":
                    self.pref_thumbnail_preview.setChecked(1)
                else:
                    self.pref_thumbnail_preview.setChecked(0)
            except:
                error_reading_configparameter(self)
            try:
                self.def_creator.setText(config.get("preferences", "def_creator"))
            except:
                error_reading_configparameter(self)
            try:
                self.def_copyright.setText(config.get("preferences", "def_copyright"))
            except:
                error_reading_configparameter(self)
        
        except IOError as e: # error reading the config file itself
            print("Very first program start, updated pyexiftoolgui with added/removed setting or user deleted the config file")
            return "lensconfig_misses"
    else:
        error_reading_configparameter(self)

def read_lensconfig3(self, read_action):
    # This is the config read function for python3
    import configparser
    config = configparser.ConfigParser()
    userpath = os.path.expanduser('~')
    print(userpath)
    print(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg'))
    # First we check in the safe way for the existence of the config file
    if os.path.isfile(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg')):
        try:
            with open(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg')) as f: pass
            # If no error we can continue
            #print "no error on config check, continue"
            config.read(os.path.join(userpath, '.pyexiftoolgui', 'lensconfig.cfg'))
            try: 
                if config["preferences"]["alternate_exiftool"] == "True":
                    self.alternate_exiftool = True
                else:
                    self.alternate_exiftool = False
            except:
                error_reading_configparameter(self)  
            try:
                self.exiftooloption.setText(config["preferences"]["exiftooloption"])
            except:
                error_reading_configparameter(self)
            try:
                if config["preferences"]["pref_thumbnail_preview"] == "True":
                    self.pref_thumbnail_preview.setChecked(1)
                else:
                    self.pref_thumbnail_preview.setChecked(0)
            except:
                error_reading_configparameter(self)
            try:
                self.def_creator.setText(config["preferences"]["def_creator"])
            except:
                error_reading_configparameter(self)
            try:
                self.def_copyright.setText(config["preferences"]["def_copyright"])
            except:
                error_reading_configparameter(self)
        
        except IOError as e: # error reading the config file itself
            print("Very first program start, updated pyexiftoolgui with added/removed setting or user deleted the config file")
    else:
        error_reading_configparameter(self)

###################################################################################################################
# End of reading writing our lens config
###################################################################################################################

