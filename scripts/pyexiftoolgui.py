#!/usr/bin/env python

# pyexiftoolgui.py

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

import os, sys, platform, shlex, subprocess, webbrowser, re

import PySide
from PySide.QtCore import *
from PySide.QtGui import *


#-------------------------------------------------------------------------
# Very first check on version
if sys.version_info<(2,7,0):
     sys.stderr.write("\n\nYou need python 2.7 or later to use pyexiftoolgui\n")
     exit(1) 

# Make sure we can run pyexiftoolgui from this folder and that subfolders are added
# base_path  can give a link, realfile gives the correct location
#base_path = os.path.dirname(os.path.abspath(__file__))
realfile = os.path.realpath(__file__)
realfile_dir = os.path.dirname(os.path.abspath(realfile))


if sys.path.count(realfile_dir) == 0:
        sys.path.insert(0, realfile_dir)
else:
        sys.path.append(realfile_dir)
# Add subfolders
#sys.path.append( realfile_dir + "/scripts" )
sys.path.append( realfile_dir + "/ui")


# python helper scripts
import petgfunctions
import programinfo
import programstrings

#import image_resources.rc

from ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
# First set the menu actions
	self.mnu_action_load_images.triggered.connect(self.loadimages)
	self.action_Quit.triggered.connect(self.quit_application)
	app.aboutToQuit.connect(self.quit_application)
        self.mnu_action_pyexiftoolgui_home.triggered.connect(self.open_pyexiftoolgui_homepage)
	self.mnu_action_exiftool.triggered.connect(self.open_exiftool_homepage)
        self.mnu_action_mapcoordinates_tab.triggered.connect(self.mapcoordinates_help)
	self.mnu_action_license.triggered.connect(self.show_license)
	self.mnu_action_Donate.triggered.connect(self.open_donate_page)
        self.mnu_action_About.triggered.connect(self.show_about_window)
# Load several views, buttons, comboboxes, spinboxes and labels from main screen
        self.btn_loadimages.clicked.connect(self.loadimages)
        self.showimagebutton.clicked.connect(self.showimage)
        self.showimagebutton.setEnabled(False)
        self.lbl_progress.setText("")
	self.progressbar.hide()
# Load several buttons from the Edit -> GPS tab
        self.dec2dmsbutton.clicked.connect(self.convertd2dms)
        self.dms2decbutton.clicked.connect(self.convertdms2d)
        self.btn_resetgps.clicked.connect(self.clear_gps_fields)
        self.btn_copy_calc_to_gps.clicked.connect(self.copy_calc_to_gpsinput)
        self.btn_gpshelp.clicked.connect(self.gps_help)
        self.btn_gps_copyfrom.clicked.connect(self.copygpsfromselected)
        self.btn_gps_copyfrom.setEnabled(False)
        self.btn_savegps.clicked.connect(self.savegpsdata)
        self.btn_savegps.setEnabled(False)
        self.btn_mapcoordinates.clicked.connect(self.open_mapcoordinates)
# Load several buttons from the Edit -> EXIF tab
        self.btn_exifhelp.clicked.connect(self.exif_help)
        self.btn_exif_copyfrom.clicked.connect(self.copyexiffromselected)
        self.btn_exif_copyfrom.setEnabled(False)
        self.btn_saveexif.clicked.connect(self.saveexifdata)
        self.btn_saveexif.setEnabled(False)
        self.btn_resetexif.clicked.connect(self.clear_exif_fields)
        self.btn_copy_exif_defaults.clicked.connect(self.exif_defaults)
# Load several buttons from the Edit -> xmp tab
        self.btn_xmphelp.clicked.connect(self.xmp_help)
        self.btn_xmp_copyfrom.clicked.connect(self.copyxmpfromselected)
        self.btn_xmp_copyfrom.setEnabled(False)
        self.btn_savexmp.clicked.connect(self.savexmpdata)
        self.btn_savexmp.setEnabled(False)
        self.btn_resetxmp.clicked.connect(self.clear_xmp_fields)
        self.btn_copy_xmp_defaults.clicked.connect(self.xmp_defaults)
# Load several buttons from the Edit -> GPano tab
        self.btn_gpanohelp.clicked.connect(self.gpano_help)
        self.btn_gpano_copyfrom.clicked.connect(self.copygpanofromselected)
        self.btn_gpano_copyfrom.setEnabled(False)
        self.btn_savegpano.clicked.connect(self.savegpanodata)
        self.btn_savegpano.setEnabled(False)
        self.btn_resetgpano.clicked.connect(self.clear_gpano_fields)
# Load several buttons from the Preferences tab
        self.btn_preferences_save.clicked.connect(self.preferences_save)
	self.btn_preferenceshelp.clicked.connect(self.preferences_help)
	self.btn_choose_exiftool.clicked.connect(self.select_exiftool)

#------------------------------------------------------------------------
# Define a few globals and variables
        self.DebugMsg = False
        self.allDebugMsg = False
	self.logging = ""
	self.logtofile = 0
# 	self.tmpworkdir = tempfile.gettempdir() +"/pyGPSTtmp"

        self.OSplatform = platform.system()
	petgfunctions.read_config(self)
	# First clean up and recreate our temporary workspace
#	petgfunctions.remove_workspace( self )
#	try:
#		fldr = os.mkdir(self.tmpworkdir)
#	except: 
#		if self.logtofile:
#			logging.info(self.tmpworkdir + " already exists.")

#------------------------------------------------------------------------
# Initialize file paths
        self.realfile_dir  = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir    = os.path.dirname(self.realfile_dir)
        self.ui_dir        = os.path.join(self.realfile_dir, "ui")

#------------------------------------------------------------------------
# Start up functions
#        OSplatform, img_converter, enfuseprg, aisprg = petgfunctions.startup_checks(self)
#        self.OSplatform = OSplatform
        if self.allDebugMsg:
            ret = QMessageBox.about(self, "returned check values", "platform: %s\nconverter: %s\nenfuse: %s\nais: %s" % (OSplatform, img_converter, enfuseprg, aisprg))

	# Startup check for available tools
	petgfunctions.tool_check(self)


#------------------------------------------------------------------------
# General functions
    def quit_application(self):
	#petgfunctions.remove_workspace(self)
	petgfunctions.write_config(self, 0)
	self.close()

#    def set_logging(self):
#	logging.basicConfig(filename=os.path.expanduser("~/pyexiftoolgui_"+time.strftime("%Y%m%d-%H%M%S")+".log"),level=logging.DEBUG)
#	logging.info("Debug set to on: Logging started on " + time.strftime("%Y-%m-%d %H:%M"))

    def testfunc(self):
        ret = petgfunctions.startup_checks(self)

    def enableimagebuttons(self):
        self.showimagebutton.setEnabled(True)
        self.imageinfobutton.setEnabled(True)


    def loadimages(self):
        ''' load images and return a filenames arrary and a space separated string of file names within double quotes'''
        loadedimages, loadedimagesstring = petgfunctions.images_dialog(self, qApp)
        petgfunctions.loadimages(self,loadedimages, loadedimagesstring,qApp)
        # If we alread did some copying or simply working on the GPS:edit tab we need to clean it after loading new images
        #petgfunctions.clear_gps_fields(self)
#------------------------------------------------------------------------
# Menu actions/functions
    def show_about_window(self):
	self.aboutbox = QMessageBox()
	
	self.licenselabel = QLabel()
	self.licensebutton = self.aboutbox.addButton(self.tr("License"), QMessageBox.ActionRole)
	closebutton = self.aboutbox.addButton(QMessageBox.Close)

	self.licensebutton.clicked.connect(self.show_license)
	self.aboutbox.setWindowTitle("About pyexiftoolgui " + programinfo.VERSION)
	self.aboutbox.setText(programinfo.ABOUTMESSAGE)
	ret = self.aboutbox.exec_()
	
    def mapcoordinates_help(self):
        helptext = programstrings.MAPCOORDINATESHELP
        petgfunctions.help_mbox(self,"Help on Integrated Mapcoordinates.net", programstrings.MAPCOORDINATESHELP)
	
    def show_license(self):
	command_line = os.path.join(self.realfile_dir, "info_window.py") + " license"
#	command_line = os.path.join(self.script_dir, "info_window.py") + " license"
        if self.OSplatform == "Windows":
                python_exe = sys.executable
                command_line = python_exe + " " + command_line
                command_line = command_line.replace("/", "\\")
                p = subprocess.call(command_line)
        else: 
    	        args = shlex.split(command_line)
    	        p = subprocess.call(args)

    def open_pyexiftoolgui_homepage(self):
        try:
                webbrowser.open("http://panorama.dyndns.org/index.php?lang=en&subject=pyExifToolGUI&texttag=pyExifToolGUI")
        except:
		QMessageBox.critical(self, "Error!", "Unable to open the pyExifToolGUI homepage" )

    def open_exiftool_homepage(self):
	try:
		webbrowser.open("http://www.sno.phy.queensu.ca/~phil/exiftool/")
	except:
		QMessageBox.critical(self, "Error!", "Unable to open the ExifTool homepage" )

    def open_donate_page(self):
	try:
		webbrowser.open("http://members.home.nl/harryvanderwolf/pyexiftoolgui/donate.html")
	except:
		QMessageBox.critical(self, "Error!", "Unable to open the donation web page" )


#------------------------------------------------------------------------
# Help functions leading to html manual
# Stupid windows doesn't recognise Anchors when starting a html file from disk
    def gps_help(self):
	try:
             if self.OSplatform == "Windows":
                webbrowser.open(os.path.join(self.parent_dir, "manual\pyexiftoolgui.html"))
             else:
		webbrowser.open("file://" + os.path.join(self.parent_dir, "manual", "pyexiftoolgui.html#EditgpsData"))
	except:
		QMessageBox.critical(self, "Error!", "Unable to open the manual page" )

    def exif_help(self):
	try:
             if self.OSplatform == "Windows":
                webbrowser.open(os.path.join(self.parent_dir, "manual\pyexiftoolgui.html"))
             else:
		webbrowser.open("file://" + os.path.join(self.parent_dir, "manual", "pyexiftoolgui.html#EditexifData"))
	except:
		QMessageBox.critical(self, "Error!", "Unable to open the manual page" )

    def xmp_help(self):
	try:
             if self.OSplatform == "Windows":
                webbrowser.open(os.path.join(self.parent_dir, "manual\pyexiftoolgui.html"))
             else:
		webbrowser.open("file://" + os.path.join(self.parent_dir, "manual", "pyexiftoolgui.html#EditxmpData"))
	except:
		QMessageBox.critical(self, "Error!", "Unable to open the manual page" )

    def gpano_help(self):
        #petgfunctions.help_mbox(self, "Help on Edit -> GPano tab", programstrings.GPANOHELP)
	try:
             if self.OSplatform == "Windows":
                webbrowser.open(os.path.join(self.parent_dir, "manual\pyexiftoolgui.html"))
             else:
		webbrowser.open("file://" + os.path.join(self.parent_dir, "manual", "pyexiftoolgui.html#EditgpanoData"))
	except:
		QMessageBox.critical(self, "Error!", "Unable to open the manual page" )

    def preferences_help(self):
 	try:
             if self.OSplatform == "Windows":
                webbrowser.open(os.path.join(self.parent_dir, "manual\pyexiftoolgui.html"))
             else:
		webbrowser.open("file://" + os.path.join(self.parent_dir, "manual", "pyexiftoolgui.html#Preferences"))
	except:
		QMessageBox.critical(self, "Error!", "Unable to open the manual page" )

#------------------------------------------------------------------------
# Image table actions
    def showimage(self):
	selected_row = self.MaintableWidget.currentRow()
	#print "current row " + str(selected_row)
	selected_image = "\"" + self.fileNames[selected_row] + "\""
	if self.OSplatform == "Windows":
                selected_image = selected_image.replace("/", "\\")
                os.startfile(selected_image)
        elif self.OSplatform == "Darwin":
                os.system('open /Applications/Preview.app ' + selected_image)
        else:
                os.system('xdg-open ' + selected_image)

    def imageinfo(self):
        petgfunctions.imageinfo(self,qApp)
#------------------------------------------------------------------------
# This is where the minimal functions for the tabs are defined. Help functions are defined above

# Edit -> GPS tab
    def convertd2dms(self):
        petgfunctions.convertLatLong(self,"d2dms")

    def convertdms2d(self):
        petgfunctions.convertLatLong(self,"dms2d")
                            
    def clear_gps_fields(self):
        petgfunctions.clear_gps_fields(self)

    def copy_calc_to_gpsinput(self):
        petgfunctions.copy_calc_to_gpsinput(self)

    def copygpsfromselected(self):
        petgfunctions.copygpsfromselected(self,qApp)

    def savegpsdata(self):
        petgfunctions.savegpsdata(self, qApp)

    def open_mapcoordinates(self):
	try:
		webbrowser.open("http://www.mapcoordinates.net/en")
	except:
		QMessageBox.critical(self, "Error!", "Unable to open the MapCoordinates.net website" )

# Edit -> EXIF tab
    def clear_exif_fields(self):
        petgfunctions.clear_exif_fields(self)

    def copyexiffromselected(self):
        petgfunctions.copyexiffromselected(self,qApp)

    def exif_defaults(self):
        petgfunctions.copy_defaults(self, qApp, "exif")

    def saveexifdata(self):
        petgfunctions.saveexifdata(self, qApp)

# Edit -> xmp tab
    def clear_xmp_fields(self):
        petgfunctions.clear_xmp_fields(self)

    def copyxmpfromselected(self):
        petgfunctions.copyxmpfromselected(self,qApp)

    def xmp_defaults(self):
        petgfunctions.copy_defaults(self, qApp, "xmp")

    def savexmpdata(self):
        petgfunctions.savexmpdata(self, qApp)

# Edit -> GPano tab
    def clear_gpano_fields(self):
        petgfunctions.clear_gpano_fields(self)

    def copygpanofromselected(self):
        petgfunctions.copygpanofromselected(self,qApp)

    def savegpanodata(self):
        petgfunctions.savegpanodata(self, qApp)

# Preferences tab
    def select_exiftool(self):
        select_exiftool = QFileDialog(self)
        qApp.processEvents()
        select_exiftool.setFileMode(QFileDialog.ExistingFile)
        select_exiftool.setViewMode(QFileDialog.Detail)
        if select_exiftool.exec_():
           files_list = select_exiftool.selectedFiles()
           print "files_list[0]" + str(files_list[0])
           self.exiftooloption.setText(files_list[0])
           return files_list[0]
        else:
           # user canceled
           self.lbl_progress.setText("you canceled the exiftool selection.")
           return ""

    def preferences_save(self):
        petgfunctions.write_config(self, 0)

#------------------------------------------------------------------------
#------------------------------------------------------------------------
# This is where the main app is started

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
