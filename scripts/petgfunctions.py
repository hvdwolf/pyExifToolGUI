# -*- coding: utf-8 -*-

# gpstfunctions.py - This python "helper" script holds a lot of functions

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

import os, sys, platform, shlex, subprocess, time, re, string

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

import programinfo
import programstrings
     

#------------------------------------------------------------------------
# All kind of functions

###################################################################################################################
# Start of Startup checks and configuration
###################################################################################################################
def remove_workspace( self ):
	# Remove our temporary workspace
#	try:
#		fls = os.remove(self.tmpworkdir + "/*")
#	except:
#		print("No files in " + self.tmpworkdir + " or no folder at all")
#	try: 
#		fldr = os.rmdir(self.tmpworkdir)
#	except:
#		print("Couldn't remove folder")
	print self.tmpworkdir
	if self.OSplatform == "Windows":
                self.tmpworkdir = self.tmpworkdir.replace("/", "\\")
                command_line = "rmdir /S /Q " + self.tmpworkdir
        else:
                command_line = "rm -rf " + self.tmpworkdir
        p = os.system(command_line)
	#args = shlex.split(command_line)
	#print args
	#p = subprocess.call(args, shell=True)

	if p == 0:
		print("Removed " + self.tmpworkdir + " and it contents.")
	else:
		print("Error removing " + self.tmpworkdir + " and it contents.")

def is_executable(fpath):
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def check_for_program(program):
	exists = False
	for path in os.environ["PATH"].split(os.pathsep):
		path_plus_program = os.path.join(path, program)
		if is_executable(path_plus_program):
			print "program " + program + " found"
			exists = True
	return exists
# End of function check_for_program and is_executable (mini sub for check_for_program)


def tool_check( self ):
	# We need this startup check as long as we don't have a package
	# that deals with dependencies

        if self.alternate_exiftool == True:
                self.exiftoolprog = self.exiftooloption.text()
        else:
                self.exiftoolprog = "exiftool"
	# Check for exiftool
	if (self.OSplatform in ("Windows", "win32")):
                print "On windows we expect exiftool.exe or exiftool(-k).exe in the pyexiftoolgui\exiftool folder"
                self.exiftool_dir = os.path.join(self.realfile_dir, "exiftool", "exiftool.exe")
                #self.exiftoolprog = self.exiftool_dir + "\exiftool.exe"
                if not os.path.isfile(self.exiftoolprog):
                       ret = QMessageBox.critical(self, "exiftool is missing or incorrectly configured", "exiftool is missing or incorrectly configured in Preferences!\nThis tool is an absolute must have!\nPlease set the correct location or install exiftool first.")
                       result = self.select_exiftool()
                       print str(result)
                       if result == "":
                          ret = QMessageBox.critical(self, "Canceled exiftool selection", "You canceled the exiftool selection.\nThe program will quit!\nFirst install exiftool or restart this program and select the correct exiftool.")
                          sys.exit()
                       else:
                          self.exiftoolprog = result
                print self.exiftoolprog
                args = self.exiftoolprog + " -ver"
        else:
	        if not check_for_program(self.exiftoolprog):
		       ret = QMessageBox.critical(self, "exiftool is missing or incorrectly configured", "exiftool is missing or incorrectly configured in Preferences!\nThis tool is an absolute must have!\nPlease set the correct location or install exiftool first.")
		       #sys.exit()
                       result = self.select_exiftool()
                       print str(result)
                       if result == "":
                          ret = QMessageBox.critical(self, "Canceled exiftool selection", "You canceled the exiftool selection.\nThe program will quit!\nFirst install exiftool or restart this program and select the correct exiftool.")
                          sys.exit()
                       else:
		          self.exiftoolprog = result
                          #print "result 2" + self.exiftoolprog
                command_line = self.exiftoolprog + " -ver"
                args = shlex.split(command_line)
        self.exiftoolversion = subprocess.check_output(args)
        # remove last character which is the final ending \n (where \ is only the escape character)        
        self.exiftoolversion = self.exiftoolversion[:-1]

        if float(self.exiftoolversion) < 9.07:
           self.lbl_progress.setText("I will disable the GPano options as exiftool >=9.07 is required. You have " + self.exiftoolversion)
           self.lbl_exiftool_to_low.setText("Your exiftool version is " + self.exiftoolversion + " . You need >=9.07 to write to images.")
           self.lbl_exiftool_to_low_2.setText("Exiftool and therefore pyExifToolGUI can read the tags. See the View Data tab.")
        else:
           self.lbl_progress.setText("Your exiftoolversion is " + self.exiftoolversion)
        #print "exiftoolversion : " + self.exiftoolversion
# End of function tool_check

def write_config(self, aftererror):
        if sys.version_info>(3,0,0):
          print "We are on python 3"
          import configparser
	  config = configparser.RawConfigParser()
        elif sys.version_info<(2,7,0):
          sys.stderr.write("\n\nYou need python 2.7 or later to use pyexiftoolgui\n")
          exit(1) 
        else: # 2.7.0 < version < 3.0.0
          import ConfigParser
	  config = ConfigParser.RawConfigParser()

	# Here we write to our pyexiftoolgui config file
	#print "Writing our config file"

	# Create our config
	config.add_section("main")
	if aftererror == 1: # Some error occurred. Go back to defaults
		config.set("main", "alternate_exiftool", str(False))
		self.alternate_exiftool = False
		config.set("main", "exiftooloption", "exiftool")
	else:
		if self.exiftooloption.text() in ("exiftool", ""):
			config.set("main", "alternate_exiftool", str(False))
			config.set("main", "exiftooloption", "exiftool")
		else: # user has changed it
			config.set("main", "alternate_exiftool", str(True))
			config.set("main", "exiftooloption", self.exiftooloption.text())
	userpath = os.path.expanduser('~')
	try:
		fldr = os.mkdir(os.path.join(userpath, '.pyexiftoolgui'))
		#print "fldr gives: " + fldr
	except:
		print "config folder already exists: no problem"
	try:
		with open(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg'), 'wb') as configfile:
			config.write(configfile)
	except:
		print "couln't write configfile"

def error_reading_configparameter(self):
	message = ("Somehow I encountered an error reading the config file.\n"
		   "This can happen when:\n- an updated version added or removed a parameter\n"
		   "- when the config file somehow got damaged.\n"
                   "- when this is the very first program start.\n\n"
		   "I will simply create a new config file. Please "
		   "check your preferences.")
	ret = QMessageBox.warning(self, "error reading config", message) 
	# simply run the write_config function to create our initial config file
	aftererror = True
	write_config(self, 1)

def read_config(self):
        if sys.version_info>(3,0,0):
          print "We are on python 3"
          import configparser
	  config = configparser.RawConfigParser()
        elif sys.version_info<(2,7,0):
          sys.stderr.write("\n\nYou need python 2.7 or later to use pyexiftoolgui\n")
          exit(1) 
        else: # 2.7.0 < version < 3.0.0
          import ConfigParser
	  config = ConfigParser.RawConfigParser()

	# Here we write to our pyexiftoolgui config file
	#print "Reading our config file"
	userpath = os.path.expanduser('~')
	print userpath
	print os.path.join(userpath, '.pyexiftoolgui', 'config.cfg')
	# First we check in the safe way for the existence of the config file
	if os.path.isfile(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg')):
	   try:
   		with open(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg')) as f: pass
		# If no error we can continue
		#print "no error on config check, continue"
		config.read(os.path.join(userpath, '.pyexiftoolgui', 'config.cfg'))
		try: 
			self.alternate_exiftool = config.getboolean("main", "alternate_exiftool")
		except:
			error_reading_configparameter(self)  
		try:
			self.exiftooloption.setText(config.get("main", "exiftooloption"))
		except:
			error_reading_configparameter(self)
		
	   except IOError as e: # error reading the config file itself
   		print "Very first program start, updated pyexiftoolgui with added/removed setting or user deleted the config file"
   	else:
           error_reading_configparameter(self)

###################################################################################################################
# End of Startup checks and configuration
###################################################################################################################

#------------------------------------------------------------------------
# General help messagebox
def help_mbox(self,helptitle, helptext):
    self.helpmbox = QMessageBox()
    self.helpmbox.setWindowTitle(helptitle)
    self.helpmbox.setText(helptext)
    ret = self.helpmbox.exec_()
#------------------------------------------------------------------------
# image functions
def images_dialog(self, qApp):
    loadedimages = QFileDialog(self)
    qApp.processEvents()
    loadedimages.setFileMode(QFileDialog.ExistingFiles)
    if self.OSplatform == "Darwin":
            loadedimages.setDirectory(os.path.expanduser('~/Pictures'))
    elif self.OSplatform == "Linux":
            loadedimages.setDirectory(os.path.expanduser('~/Pictures'))
    elif self.OSplatform == "Windows":
            loadedimages.setDirectory(os.path.expanduser('~/My Pictures'))

    qApp.processEvents()
    self.lbl_progress.setText("Loading images")
    qApp.processEvents()
#    loadedimages.setNameFilter("image files (*.jpg *.tif *.tiff *.png)\nAll Files (*.*)")
    loadedimages.setNameFilter("image files (" + programstrings.SUPPORTEDIMAGES + ")\nAll Files (*.*)")
    loadedimages.setViewMode(QFileDialog.Detail)
    filenamesstring = ""
    if loadedimages.exec_():
        fileNames = loadedimages.selectedFiles()
        qApp.processEvents()
        for fileName in fileNames:
           # Make sure that spaces in path/file names etcetera are
           # covered by putting them within spaces
	   #print fileName
           filenamesstring += "\"" + fileName + "\" "
        #ret= QMessageBox.about(self, "file names", """ %s""" % fnstring)
        #return fileNames
        self.fileNames = fileNames
        self.filenamesstring = filenamesstring
    else:
	# user canceled
	self.lbl_progress.setText("you canceled loading the images.")
	fileNames = ""
    return (fileNames, filenamesstring)


def loadimages(self,loadedimages, loadedimagesstring,qApp):
	if loadedimagesstring == "":
		# user canceled loading images
		print("user canceled loading images")
	else:
	        imagestring = ""
        	rowcounter = 0
	        total_images = len(loadedimages)
		self.progressbar.setRange(0, total_images)
	        self.progressbar.setValue(0)
	        self.progressbar.show()
	        qApp.processEvents()
        	self.MaintableWidget.clearContents()
                self.MaintableWidget.setRowCount(0)
        	#self.MaintableWidget.setRowCount(len(loadedimages))
		self.resolutions = []
        	cur_width_height = ""
        	for loadedimage in loadedimages:
        	    if self.DebugMsg:
        	        print rowcounter
        	        print loadedimage + "\n"
        	        print loadedimagesstring

                    #print "loaded image: " + loadedimage
        	    folder,imagefile = os.path.split(loadedimage)
        	    self.image_folder = folder
        	    qtablefilename = QTableWidgetItem(imagefile)
        	    # Now create the thumbnail to be displayed
        	    thumbnail = QLabel(self)
        	    image = QImage(loadedimage)
        	    thumbnail.setPixmap(QPixmap.fromImage(image))

        	    thumbnail.setScaledContents(True)
	            # Fill the table
        	    self.MaintableWidget.insertRow(rowcounter)
        	    self.MaintableWidget.setRowHeight(rowcounter,75)
        	    self.MaintableWidget.setColumnWidth(0,75)
        	    self.MaintableWidget.setColumnWidth(1,225)
        	    self.MaintableWidget.setCellWidget(rowcounter, 0, thumbnail)
        	    self.MaintableWidget.setItem(rowcounter, 1, qtablefilename)
                    self.MaintableWidget.setToolTip('image(s) folder: ' + folder)
        	    rowcounter += 1
        	    self.progressbar.setValue(rowcounter) 
        	    self.lbl_progress.setText("Creating thumbnail of: " + os.path.basename(loadedimage))
        	    qApp.processEvents()
        	    imagestring += loadedimage + " "
        	if self.allDebugMsg:
        	    ret= QMessageBox.about(self, "file names", "images found \n %s" % loadedimagesstring)
        	    ret= QMessageBox.about(self, "file names", "images found 2 \n %s" % imagestring)
        	#self.imagesfolderlineitem.setText(folder)
                # enable buttons that can only work once we have images loaded
        	self.showimagebutton.setEnabled(True)
                self.btn_gps_copyfrom.setEnabled(True)
                self.btn_savegps.setEnabled(True)
                self.btn_exif_copyfrom.setEnabled(True)
                self.btn_saveexif.setEnabled(True)
                if float(self.exiftoolversion) > 9.06:
                   self.btn_gpano_copyfrom.setEnabled(True)
                   self.btn_savegpano.setEnabled(True)
        	self.progressbar.hide()
                self.lbl_progress.setText("Click thumb or filename to display the image info")
                # Set proper events
                self.MaintableWidget.cellClicked.connect(self.imageinfo)
		self.radioButton_all.clicked.connect(self.imageinfo)
		self.radioButton_exif.clicked.connect(self.imageinfo)
		self.radioButton_xmp.clicked.connect(self.imageinfo)
		self.radioButton_iptc.clicked.connect(self.imageinfo)
		self.radioButton_gps.clicked.connect(self.imageinfo)
		self.radioButton_gpano.clicked.connect(self.imageinfo)
		self.radioButton_makernotes.clicked.connect(self.imageinfo)




def imageinfo(self, qApp):
        self.lbl_progress.setText("")
	selected_row = self.MaintableWidget.currentRow()
	selected_image = "\"" + self.fileNames[selected_row] + "\""
        if self.radioButton_all.isChecked():
            exiftool_params = ""
            arguments = " -a "
            header = "all tags"
        if self.radioButton_exif.isChecked():
            exiftool_params = "-exif:all"
            header = "EXIF tags"
        if self.radioButton_xmp.isChecked():
            exiftool_params = "-xmp:all"
            header = "XMP tags"
        if self.radioButton_iptc.isChecked():
            exiftool_params = "-iptc:all"
            header = "IPTC tags"
        if self.radioButton_gps.isChecked():
            exiftool_params = "-gps:all -xmp:GPSLatitude -xmp:GPSLongitude -xmp:Location -xmp:Country -xmp:State -xmp:City"
            arguments = " -a -gps:all -xmp:GPSLatitude -xmp:GPSLongitude -xmp:Location -xmp:Country -xmp:State -xmp:City"
            header = "GPS tags"
        if self.radioButton_gpano.isChecked():
            exiftool_params = "-xmp:CroppedAreaImageHeightPixels -xmp:CroppedAreaImageWidthPixels -xmp:CroppedAreaLeftPixels -xmp:CroppedAreaTopPixels -xmp:FullPanoHeightPixels -xmp:FullPanoWidthPixels -xmp:ProjectionType -xmp:UsePanoramaViewer -xmp:PoseHeadingDegrees"
            arguments = " -xmp:CroppedAreaImageHeightPixels -xmp:CroppedAreaImageWidthPixels -xmp:CroppedAreaLeftPixels -xmp:CroppedAreaTopPixels -xmp:FullPanoHeightPixels -xmp:FullPanoWidthPixels -xmp:ProjectionType -xmp:UsePanoramaViewer -xmp:PoseHeadingDegrees"
            header = "GPano tags"
        if self.radioButton_makernotes.isChecked():
            exiftool_params = "-makernotes:all"
            header = "makernotes tags"
        #self.lbl_progress.setText("image info of: " + selected_image)
        if self.OSplatform == "Windows":
                selected_image = selected_image.replace("/", "\\")
                args = self.exiftoolprog + " -a " + exiftool_params + " " + selected_image
        else:
                command_line = self.exiftoolprog + " -a " + exiftool_params + " " + selected_image
                args = shlex.split(command_line)
        #print "command line is: " + command_line
        #print "args are: " + args
        p = subprocess.check_output(args, universal_newlines=True)
        #arguments = arguments + " " + selected_image
        #print "ET = " + self.exiftoolprog + " arguments are " + arguments
        #myprocess = QProcess(self)
        #myprocess.start(self.exiftoolprog, arguments)
        #myprocess.waitForFinished(-1)
        #p = myprocess.readAll()
        #print "p after myprocess"
        #print p
        if len(p) == 0:
           p = header + "   :   No data available\n"
           #print p
        # remove last character which is the final ending \n (where \ is only the escape character)        
        p = p[:-1]
        p_lines = re.split('\n',p)
        self.exiftableWidget.clearContents()
	self.exiftableWidget.setRowCount(0)
        rowcounter = 0
        for line in p_lines:
            try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               #print "descriptor " + descriptor + " ;description " + description
               self.exiftableWidget.insertRow(rowcounter)
               self.exiftableWidget.setColumnWidth(0,225)
               self.exiftableWidget.setColumnWidth(1,325)
               self.exiftableWidget.setItem(rowcounter, 0, QTableWidgetItem(descriptor))
               self.exiftableWidget.setItem(rowcounter, 1, QTableWidgetItem(description))
               rowcounter += 1
               qApp.processEvents()
            except:
               print "always the last line that doesn't work"



#------------------------------------------------------------------------
# Edit -> Gps tab and actions
def convertLatLong(self, direction):
    # only "int" at the latest moment or calculations go wrong
    if direction == 'dms2d':
       # first latitude
       # Note that "South" latitudes and "West" longitudes convert to negative decimal numbers
       if int(self.calc_lat_sec.text()) in range(0, 60):
          latd = float(self.calc_lat_sec.text()) / float(60)
       else:
          ret = QMessageBox.critical(self, "seconds error", "seconds must fall in the range 0 to <60")
       if int(self.calc_lat_min.text()) in range(0, 60):
         latd = (int(self.calc_lat_min.text()) + latd) / float(60)
       else:
         ret = QMessageBox.critical(self, "minutes error", "minutes must fall in the range 0 to <60")
       # check whether lat degrees falls within 0 and 89
       if int(self.calc_lat_deg.text()) in range(0, 90):
         latd = latd + int(self.calc_lat_deg.text())
       else:
         ret = QMessageBox.critical(self, "degrees error", "Latitude degrees must fall in the range 0 to 89")
       if self.radioButton_calc_gpsS.isChecked(): # South
         # this means a negative decimal latitude
         latd = -(latd)
       self.calc_latitude.setText(str(round(latd,6)))
       # now longitude
       if int(self.calc_lon_sec.text()) in range(0, 60):
         lond = float(self.calc_lon_sec.text()) / float(60)
       else:
         ret = QMessageBox.critical(self, "seconds error", "seconds must fall in the range 0 to <60")
       if int(self.calc_lon_min.text()) in range(0, 60):
         lond = (int(self.calc_lon_min.text()) + lond) / float(60)
       else:
         ret = QMessageBox.critical(self, "minutes error", "minutes must fall in the range 0 to <60")
       # check whether lon degrees falls within 0 and 179
       if int(self.calc_lon_deg.text()) in range(0, 179):
         lond = lond + int(self.calc_lon_deg.text())
       else:
         ret = QMessageBox.critical(self, "degrees error", "Longitude degrees must fall in the range 0 to 179")
       if self.radioButton_calc_gpsW.isChecked(): # West
         lond = -(lond)
       # Update value in decimal latituted field
       self.calc_longitude.setText(str(round(lond,6)))
    else: # direction is d2dms
       # First latitude
       latitude = self.calc_latitude.text()
       # First check on "," in string
       if "," in latitude:
          latitude = latitude.replace(',','.')
          self.calc_latitude.setText(latitude)
       # Now check whether we have a "." in our strong. If not we have an integer and re is not necessary
       if "." in latitude:
         latint, latremain = re.split('\.', latitude)
       else:
         latint = latitude
       if int(latint) in range (-89, 89):
         if (int(latint)) < 0:
                 latint = -(int(latint))
                 latitude = -(float(latitude))
                 self.radioButton_calc_gpsS.setChecked(1)
         else:
                 self.radioButton_calc_gpsN.setChecked(1)

         deg = str(latint)
         self.calc_lat_deg.setText(deg)
         min = (float(latitude) - int(deg)) * 60
         self.calc_lat_min.setText(str(int(min)))
         sec = int(round(((float(min) - int(min)) *60), 0))
         self.calc_lat_sec.setText(str(sec))
       else:
         ret = QMessageBox.critical(self, "degrees error", "Latitude decimal must fall in the range -90 < degr < 90")
       # Now longitude
       longitude = self.calc_longitude.text()
       # First check on "," in string
       if "," in longitude:
          longitude = longitude.replace(',','.')
          self.calc_longitude.setText(longitude)
       # Now check whether we have a "." in our strong. If not we have an integer and re is not necessary
       if "." in longitude:
          lonint, lonremain = re.split('\.',(self.calc_longitude.text()))
       else:
          lonint = longitude
       if int(lonint) in range (-179, 179):
         if (int(lonint)) < 0:
                 lonint = -(int(lonint))
                 longitude = -(float(longitude))
                 self.radioButton_calc_gpsW.setChecked(1)
         else:
                 self.radioButton_calc_gpsE.setChecked(1)
         #longitude = float(lonint) + (float(lonremain)/(10**multiplier))
         deg = str(lonint)
         self.calc_lon_deg.setText(deg)
         min = (float(longitude) - int(deg)) * 60
         self.calc_lon_min.setText(str(int(min)))
         sec = int(round(((float(min) - int(min)) *60), 0))
         self.calc_lon_sec.setText(str(sec))
       else:
         ret = QMessageBox.critical(self, "degrees error", "Longitude decimal must fall in the range -180 < degr < 180")

def clear_gps_fields(self):
        self.calc_lat_deg.setText("")
        self.calc_lat_min.setText("")
        self.calc_lat_sec.setText("")
        self.calc_latitude.setText("")
        self.radioButton_calc_gpsN.setChecked(1)
        self.calc_lon_deg.setText("")
        self.calc_lon_min.setText("")
        self.calc_lon_sec.setText("")
        self.calc_longitude.setText("")
        self.gps_lat_decimal.setText("")
        self.gps_lon_decimal.setText("")
        self.radioButton_calc_gpsE.setChecked(1)
        self.gps_altitude.setText("")
        self.chk_AboveSeaLevel.setChecked(1)
        self.gps_lat_deg.setText("")
        self.gps_lat_min.setText("")
        self.gps_lat_sec.setText("")
        self.gps_lon_deg.setText("")
        self.gps_lon_min.setText("")
        self.gps_lon_sec.setText("")
        self.radioButton_gpsN.setChecked(1)
        self.radioButton_gpsE.setChecked(1)
        self.xmp_location.setText("")
        self.xmp_country.setText("")
        self.xmp_state.setText("")
        self.xmp_city.setText("")
        self.chk_xmp_location.setChecked(1)
        self.chk_xmp_country.setChecked(1)
        self.chk_xmp_state.setChecked(1)
        self.chk_xmp_city.setChecked(1)
        self.gps_timestamp.setText("")
        self.gps_datestamp.setText("")
        self.gps_versionid.setText("")
        self.gps_mapdatum.setText("")
        self.chk_gps_timestamp.setChecked(1)
        self.chk_gps_datestamp.setChecked(1)

def copy_calc_to_gpsinput(self):
        self.gps_lat_decimal.setText(self.calc_latitude.text())
        self.gps_lon_decimal.setText(self.calc_longitude.text())
        self.gps_lat_deg.setText(self.calc_lat_deg.text())
        self.gps_lat_min.setText(self.calc_lat_min.text())
        self.gps_lat_sec.setText(self.calc_lat_sec.text())
        self.gps_lon_deg.setText(self.calc_lon_deg.text())
        self.gps_lon_min.setText(self.calc_lon_min.text())
        self.gps_lon_sec.setText(self.calc_lon_sec.text())
        if self.radioButton_calc_gpsN.isChecked():
		self.radioButton_gpsN.setChecked(1)
        else:
		self.radioButton_gpsS.setChecked(1)
        if self.radioButton_calc_gpsE.isChecked():
		self.radioButton_gpsE.setChecked(1)
        else:
		self.radioButton_gpsW.setChecked(1)


def d2dms(self, value, sort):
        # This is a simplified one-way copy of the convertLatLong function above for the input read-only fields
        # Both cold be integrated, more efficient, but this is faster to maintain (and I'm lazy)
        value = abs(float(value))
        deg = int(value)
        min = (float(value) - int(deg)) * 60
        sec = int(round(((float(min) - int(min)) *60), 0))
        # only "int" at the latest moment or calculations go wrong
        if sort == "lat":
           self.gps_lat_deg.setText(str(deg))
           self.gps_lat_min.setText(str(int(min)))
           self.gps_lat_sec.setText(str(sec))
        else:
           self.gps_lon_deg.setText(str(deg))
           self.gps_lon_min.setText(str(int(min)))
           self.gps_lon_sec.setText(str(sec))
       

def copygpsfromselected(self,qApp):
        # First clean input fields
        clear_gps_fields(self)
        exiftool_params = ' -e -n -a -gps:all -xmp:Location -xmp:Country -xmp:State -xmp:City -xmp:GPSLatitude -xmp:GPSLongitude '
        data = True
        p = read_exif_info(self, exiftool_params)
        if len(p) == 0:
           data = False
           message = ("<p>You are trying to copy the gps/location info from your source image, but your source image "
                      "doesn't contain data or doesn't seem to contain data (or you didn't select an image).</p>"
                      "<p>In case your camera has a GPS system, but only uses it's internal \"maker\" options "
                      "to store the gps data, I can't retrieve the data as it is stored differently "
                      "for every brand of camera.</p>"
                      "<p>If this is the case for your camera, your only option is to copy & paste the information out "
                      "of the table rows from the \"General\" tab.")
           ret = QMessageBox.warning(self, "Error copying gps info from source image", message)
        else:
           # remove last character which is the final ending \n (where \ is only the escape character)        
           p = p[:-1]
           p_lines = re.split('\n',p)
           rowcounter = 0
           for line in p_lines:
            #try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               gpslat = 0
               gpslon = 0
               latref = 0
               lonref = 0
               if descriptor == "GPS Version ID":
                     self.gps_versionid.setText(description)
               if descriptor == "GPS Latitude Ref":
                  latref = 1
                  latrefvalue = description
                  if description == "N":
                     self.radioButton_gpsN.setChecked(1)
                  else:
                     self.radioButton_gpsS.setChecked(1)
               if descriptor == "GPS Latitude":
                     gpslat += 1
                     if gpslat == 2:
                        print "we have a xmp latitude"
                     gpslatvalue = description
                     self.gps_lat_decimal.setText(str(round(float(description),6)))
               if descriptor == "GPS Longitude Ref":
                  lonref = 1
                  lonrefvalue = description
                  if description == "E":
                     self.radioButton_gpsE.setChecked(1)
                  else:
                     self.radioButton_gpsW.setChecked(1)
               if descriptor == "GPS Longitude":
                      gpslon += 1
                      if gpslon == 2:
                         print "we have an xmp longitude"
                      gpslonvalue = description
                      self.gps_lon_decimal.setText(str(round(float(description),6)))
               if descriptor == "GPS Altitude Ref":
                  if description == "0":
                     self.chk_AboveSeaLevel.setChecked(1)
                  else:
                     self.chk_AboveSeaLevel.setChecked(0)
               if descriptor == "GPS Altitude":
                      self.gps_altitude.setText(str(round(float(description),1)))
               if descriptor == "Location":
                     self.xmp_location.setText(description)
               if descriptor == "Country":
                     self.xmp_country.setText(description)
               if descriptor == "State":
                     self.xmp_state.setText(description)
               if descriptor == "City":
                     self.xmp_city.setText(description)
               if descriptor == "GPS Time Stamp":
                     self.gps_timestamp.setText(description)
               if descriptor == "GPS Date Stamp":
                     self.gps_datestamp.setText(description)
               if descriptor == "GPS Map Datum":
                     self.gps_mapdatum.setText(description)
               #print "rowcounter " + str(rowcounter) + " descriptor " + descriptor + " ;description " + description
               rowcounter += 1
               #qApp.processEvents()
            #except:
               #print "always the last line that doesn't work"

        # We bluntly walk through all tags as we don't know whether they are complete.
        # Now we need to check for neg/pos latitutes and longitudes by REF values as
        # We do not know now whether we have exif decimal values (always positive)
        # or xmp decimal values which can be negative or positive.
        # That's not so elegant but much simpler then building internal checks.
        if latref == 1:
           value = self.gps_lat_decimal.text()
           if latrefvalue == "N":
               self.gps_lat_decimal.setText(str(abs(float(value))))
           else: # E = negative
               if value.count('-') == 0: # doesn't contain a - but should contain it.
                  self.gps_lat_decimal.setText('-' + value)
        if lonref == 1:
           value = self.gps_lon_decimal.text()
           if latrefvalue == "E":
               self.gps_lon_decimal.setText(str(abs(float(value))))
           else: # W = negative
               if value.count('-') == 0: # doesn't contain a - but should contain it.
                  self.gps_lon_decimal.setText('-' + value)
        # Check whether we have xmp lat/lon
        if data:
           d2dms(self, gpslatvalue, "lat")
           d2dms(self, gpslonvalue, "lon")

def savegpsdata(self, qApp):
        # Exif and xmp gps data
        if self.chk_lat_lon_alt.isChecked():
            exiftool_params =  ' -exif:GPSLatitude="' + self.gps_lat_decimal.text() + '" '
            value = float(self.gps_lat_decimal.text())
            if value > 0:
                exiftool_params +=  ' -exif:GPSLatitudeREF="N" '
            else:
                exiftool_params +=  ' -exif:GPSLatitudeREF="S" '
            exiftool_params +=  ' -xmp:GPSLatitude="' + self.gps_lat_decimal.text() + '" '
            exiftool_params +=  ' -exif:GPSLongitude="' + self.gps_lon_decimal.text() + '" '
            value = float(self.gps_lon_decimal.text())
            if value > 0:
                exiftool_params +=  ' -exif:GPSLongitudeREF="E" '
            else:
                exiftool_params +=  ' -exif:GPSLongitudeREF="W" '
            exiftool_params +=  ' -xmp:GPSLongitude="' + self.gps_lon_decimal.text() + '" '
            exiftool_params +=  ' -exif:GPSAltitude="' + self.gps_altitude.text() + '" '
            exiftool_params +=  ' -xmp:GPSAltitude="' + self.gps_altitude.text() + '" '
            if self.chk_AboveSeaLevel.isChecked():
                exiftool_params +=  ' -exif:GPSAltitudeRef= "0" '  # Above sea level
            else:
                exiftool_params +=  ' -exif:GPSAltitudeRef= "1" '  # Below sea level
        # Location data for XMP and IPTC
        if self.chk_xmp_location.isChecked():
               exiftool_params +=  '-xmp:Location="' + self.xmp_location.text() + '" '
               exiftool_params +=  '-iptc:Sub-location="' + self.xmp_location.text() + '" '
        if self.chk_xmp_country.isChecked():
               exiftool_params +=  '-xmp:Country="' + self.xmp_country.text() + '" '
               exiftool_params +=  '-iptc:Country-PrimaryLocationName="' + self.xmp_country.text() + '" '
        if self.chk_xmp_state.isChecked():
               exiftool_params +=  '-xmp:State="' + self.xmp_state.text() + '" '
               exiftool_params +=  '-iptc:Province-State="' + self.xmp_state.text() + '" '
        if self.chk_xmp_city.isChecked():
               exiftool_params +=  '-xmp:City="' + self.xmp_city.text() + '" '
               exiftool_params +=  '-iptc:City="' + self.xmp_city.text() + '" '
        # Map date/time and format stuff
        if self.chk_gps_timestamp.isChecked():
               exiftool_params +=  '-exif:Copyright="' + self.exif_Copyright.text() + '" '
        if self.chk_gps_datestamp.isChecked():
               exiftool_params +=  '-exif:UserComment="' + self.exif_UserComment.text() + '" '
        if self.gps_mapdatum.text() == "":
               exiftool_params +=  '-exif:GPSMapDatum="WGS-84" '
        else:
               exiftool_params +=  '-exif:GPSMapDatum="' + self.gps_mapdatum.text() + '" '
        print exiftool_params
        # Now write the data to the photo(s)
        write_exif_info(self, exiftool_params, qApp)

#------------------------------------------------------------------------
# Edit -> Exif tab and actions
def clear_exif_fields(self):
        self.exif_Make.setText("")
        self.exif_Model.setText("")
        self.exif_ModifyDate.setText("")
        self.exif_DateTimeOriginal.setText("")
        self.exif_CreateDate.setText("")
        self.exif_Artist.setText("")
        self.exif_Copyright.setText("")
        self.exif_UserComment.setText("")
        self.exif_ImageDescription.clear()

        self.chk_exif_Make.setChecked(1)
        self.chk_exif_Model.setChecked(1)
        self.chk_exif_ModifyDate.setChecked(1)
        self.chk_exif_DateTimeOriginal.setChecked(1)
        self.chk_exif_CreateDate.setChecked(1)
        self.chk_exif_Artist.setChecked(1)
        self.chk_exif_Copyright.setChecked(1)
        self.chk_exif_UserComment.setChecked(1)
        self.chk_exif_ImageDescription.setChecked(1)

def copyexiffromselected(self,qApp):
        # First clean input fields
        clear_exif_fields(self)
        exiftool_params = ' -e -n -exif:Make -exif:Model -exif:ModifyDate -exif:DateTimeOriginal -exif:CreateDate -exif:Artist -exif:Copyright -exif:UserComment -exif:ImageDescription '
        p = read_exif_info(self, exiftool_params)
        if len(p) == 0:
           data = False
           message = ("<p>You are trying to copy exif info from your source image, but your source image "
                      "doesn't contain the specified exif data or doesn't seem to contain any exif data (or you didn't select an image).</p>")
           ret = QMessageBox.warning(self, "Error copying exif info from source image", message)
        else:
           # remove last character which is the final ending \n (where \ is only the escape character)        
           p = p[:-1]
           p_lines = re.split('\n',p)
           rowcounter = 0
           for line in p_lines:
            #try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               gpslat = 0
               gpslon = 0
               if descriptor == "Make":
                     self.exif_Make.setText(description)
               if descriptor == "Camera Model Name":
                     self.exif_Model.setText(description)
               if descriptor == "Modify Date":
                     self.exif_ModifyDate.setText(description)
               if descriptor == "Date/Time Original":
                      self.exif_DateTimeOriginal.setText(description)
               if descriptor == "Create Date":
                     self.exif_CreateDate.setText(description)
               if descriptor == "Artist":
                     self.exif_Artist.setText(description)
               if descriptor == "Copyright":
                     self.exif_Copyright.setText(description)
               if descriptor == "User Comment":
                     self.exif_UserComment.setText(description)
               if descriptor == "Image Description":
                     self.exif_ImageDescription.insertPlainText(description)
               #print "rowcounter " + str(rowcounter) + " descriptor " + descriptor + " ;description " + description
               rowcounter += 1

def saveexifdata(self, qApp):
        if self.chk_exif_Make.isChecked():
               exiftool_params =  ' -exif:Make="' + self.exif_Make.text() + '" '
        if self.chk_exif_Model.isChecked():
               exiftool_params +=  '-exif:Model="' + self.exif_Model.text() + '" '
        if self.chk_exif_ModifyDate.isChecked():
               exiftool_params +=  '-exif:ModifyDate="' + self.exif_ModifyDate.text() + '" '
        if self.chk_exif_DateTimeOriginal.isChecked():
               exiftool_params +=  '-exif:DateTimeOriginal="' + self.exif_DateTimeOriginal.text() + '" '
        if self.chk_exif_CreateDate.isChecked():
               exiftool_params +=  '-exif:CreateDate="' + self.exif_CreateDate.text() + '" '
        if self.chk_exif_Artist.isChecked():
               exiftool_params +=  '-exif:Artist="' + self.exif_Artist.text() + '" '
        if self.chk_exif_Copyright.isChecked():
               exiftool_params +=  '-exif:Copyright="' + self.exif_Copyright.text() + '" '
        if self.chk_exif_UserComment.isChecked():
               exiftool_params +=  '-exif:UserComment="' + self.exif_UserComment.text() + '" '
        if self.chk_exif_ImageDescription.isChecked():
               ImgDescr = self.exif_ImageDescription.toPlainText()
               exiftool_params +=  '-exif:ImageDescription="' + ImgDescr + '" '

        write_exif_info(self, exiftool_params, qApp)
               
#------------------------------------------------------------------------
# Edit -> GPano tab and actions
def clear_gpano_fields(self):
        self.xmp_CroppedAreaImageHeightPixels.setText("")
        self.xmp_CroppedAreaImageWidthPixels.setText("")
        self.xmp_CroppedAreaLeftPixels.setText("")
        self.xmp_CroppedAreaTopPixels.setText("")
        self.xmp_FullPanoHeightPixels.setText("")
        self.xmp_FullPanoWidthPixels.setText("")
        self.xmp_ProjectionType.setCurrentIndex(0)
        self.xmp_UsePanoramaViewer.setChecked(1)
        self.xmp_PoseHeadingDegrees.setText("")

        self.chk_xmp_CroppedAreaImageHeightPixels.setChecked(1)
        self.chk_xmp_CroppedAreaImageWidthPixels.setChecked(1)
        self.chk_xmp_CroppedAreaLeftPixels.setChecked(1)
        self.chk_xmp_CroppedAreaTopPixels.setChecked(1)
        self.chk_xmp_FullPanoHeightPixels.setChecked(1)
        self.chk_xmp_FullPanoWidthPixels.setChecked(1)
        self.chk_xmp_ProjectionType.setChecked(1)
        self.chk_xmp_UsePanoramaViewer.setChecked(1)
        self.chk_xmp_PoseHeadingDegrees.setChecked(1)

def copygpanofromselected(self,qApp):
        # First clean input fields
        clear_exif_fields(self)
        exiftool_params = ' -e -n -xmp:CroppedAreaImageHeightPixels -xmp:CroppedAreaImageWidthPixels -xmp:CroppedAreaLeftPixels -xmp:CroppedAreaTopPixels -xmp:FullPanoHeightPixels -xmp:FullPanoWidthPixels -xmp:ProjectionType -xmp:UsePanoramaViewer -xmp:PoseHeadingDegrees '
        p = read_exif_info(self, exiftool_params)
        if len(p) == 0:
           data = False
           message = ("<p>You are trying to copy GPano (Google Photosphere) info from your source image, but your source image "
                      "doesn't contain the specified GPano data or doesn't seem to contain any GPano data (or you didn't select an image).</p>")
           ret = QMessageBox.warning(self, "Error copying GPano info from source image", message)
        else:
           # remove last character which is the final ending \n (where \ is only the escape character)        
           p = p[:-1]
           p_lines = re.split('\n',p)
           rowcounter = 0
           for line in p_lines:
            #try: 
               descriptor, description = re.split(':', line,1)
               descriptor = descriptor.strip()
               description = description.strip()
               gpslat = 0
               gpslon = 0
               if descriptor == "Cropped Area Image Height Pixels":
                     self.xmp_CroppedAreaImageHeightPixels.setText(description)
               if descriptor == "Cropped Area Image Width Pixels":
                     self.xmp_CroppedAreaImageWidthPixels.setText(description)
               if descriptor == "Cropped Area Left Pixels":
                     self.xmp_CroppedAreaLeftPixels.setText(description)
               if descriptor == "Cropped Area Top Pixels":
                      self.xmp_CroppedAreaTopPixels.setText(description)
               if descriptor == "Full Pano Height Pixels":
                     self.xmp_FullPanoHeightPixels.setText(description)
               if descriptor == "Full Pano Width Pixels":
                     self.xmp_FullPanoWidthPixels.setText(description)
               if descriptor == "Projection Type":
                     if description == "equirectangular":
                        self.xmp_ProjectionType.setCurrentIndex(0)
                     elif description == "equirectangular":
                        self.xmp_ProjectionType.setCurrentIndex(1)
                     elif description == "rectilinear":
                        self.xmp_ProjectionType.setCurrentIndex(2)
               if descriptor == "Use Panorama Viewer":
                     if description == "True":
                        self.xmp_UsePanoramaViewer.setChecked(1)
                     else:
                        self.xmp_UsePanoramaViewer.setChecked(0)
               if descriptor == "Pose Heading Degrees":
                     self.xmp_PoseHeadingDegrees.setText(description)
               #print "rowcounter " + str(rowcounter) + " descriptor " + descriptor + " ;description " + description
               rowcounter += 1

def savegpanodata(self, qApp):
        if self.chk_xmp_CroppedAreaImageHeightPixels.isChecked():
               exiftool_params =  ' -xmp:CroppedAreaImageHeightPixels="' + self.xmp_CroppedAreaImageHeightPixels.text() + '" '
        if self.chk_xmp_CroppedAreaImageWidthPixels.isChecked():
               exiftool_params +=  '-xmp:CroppedAreaImageWidthPixels="' + self.xmp_CroppedAreaImageWidthPixels.text() + '" '
        if self.chk_xmp_CroppedAreaLeftPixels.isChecked():
               exiftool_params +=  '-xmp:CroppedAreaLeftPixels="' + self.xmp_CroppedAreaLeftPixels.text() + '" '
        if self.chk_xmp_CroppedAreaTopPixels.isChecked():
               exiftool_params +=  '-xmp:CroppedAreaTopPixels="' + self.xmp_CroppedAreaTopPixels.text() + '" '
        if self.chk_xmp_FullPanoHeightPixels.isChecked():
               exiftool_params +=  '-xmp:FullPanoHeightPixels="' + self.xmp_FullPanoHeightPixels.text() + '" '
        if self.chk_xmp_FullPanoWidthPixels.isChecked():
               exiftool_params +=  '-xmp:FullPanoWidthPixels="' + self.xmp_FullPanoWidthPixels.text() + '" '
        if self.chk_xmp_ProjectionType.isChecked():
               if self.xmp_ProjectionType.currentIndex == 0:
                  exiftool_params +=  '-xmp:ProjectionType="equirectangular" '
               elif self.xmp_ProjectionType.currentIndex == 1:
                  exiftool_params +=  '-xmp:ProjectionType="cylindrical" '
               elif self.xmp_ProjectionType.currentIndex == 2:
                  exiftool_params +=  '-xmp:ProjectionType="rectangular" '
        if self.chk_xmp_UsePanoramaViewer.isChecked(): 
               if self.xmp_UsePanoramaViewer.isChecked():
                  exiftool_params +=  '-xmp:UsePanoramaViewer=1 '
               else:
                  exiftool_params +=  '-xmp:UsePanoramaViewer=0 '
        if self.chk_xmp_PoseHeadingDegrees.isChecked():
               exiftool_params +=  '-xmp:PoseHeadingDegrees="' + self.xmp_PoseHeadingDegrees.text() + '" '

        write_exif_info(self, exiftool_params, qApp)


#------------------------------------------------------------------------
# Real exiftool read/write functions
def read_exif_info(self, exiftool_params):
        self.lbl_progress.setText("")
	selected_row = self.MaintableWidget.currentRow()
	selected_image = "\"" + self.fileNames[selected_row] + "\""
        if self.OSplatform in ("Windows", "win32"):
                selected_image = selected_image.replace("/", "\\")
                args = self.exiftoolprog + exiftool_params + selected_image
        else:
                command_line = self.exiftoolprog + exiftool_params + selected_image
                args = shlex.split(command_line)
        p = subprocess.check_output(args, universal_newlines=True)
        return p

def write_exif_info(self, exiftoolparams, qApp):
        mysoftware = programinfo.NAME + " " + programinfo.VERSION
        exiftoolparams = ' -overwrite_original_in_place -ProcessingSoftware="' + mysoftware + '" ' + exiftoolparams

        selected_rows = self.MaintableWidget.selectedIndexes()
        print 'number of rows ' + str(len(selected_rows))
        rowcounter = 0
        total_rows = len(selected_rows)
        self.progressbar.setRange(0, total_rows)
	self.progressbar.setValue(0)
	self.progressbar.show()
        rows = []
        for selected_row in selected_rows:
                selected_row = str(selected_row)
                selected_row = selected_row.replace("<PySide.QtCore.QModelIndex(",'')
                selected_row, tail = re.split(',0x0',selected_row)
                #print str(selected_row)
                row, column = re.split(',',selected_row)
                if row not in rows:
                        rows.append(row)
                        selected_image = "\"" + self.fileNames[int(row)] + "\""
                        print 'exiftool ' + exiftoolparams + ' ' + selected_image
                        print 'exiftool "-FileModifyDate<DateTimeOriginal" ' + selected_image
        	        rowcounter += 1
        	        self.progressbar.setValue(rowcounter) 
        	        self.lbl_progress.setText("Writing information to: " + os.path.basename(selected_image))
        	        qApp.processEvents()
                        if self.OSplatform in ("Windows", "win32"):
                           # First write the info
                           selected_image = selected_image.replace("/", "\\")
                           args = self.exiftoolprog + exiftoolparams + selected_image
                           p = subprocess.call(args)
                           # Now reset the file date
                           args = self.exiftoolprog + ' "-FileModifyDate<DateTimeOriginal" ' + selected_image
                           p = subprocess.call(args)
                        else:
                           # First write the info
                           command_line = self.exiftoolprog + exiftoolparams + selected_image
                           args = shlex.split(command_line)
                           p = subprocess.call(args)
                           # Now reset the file date
                           command_line = self.exiftoolprog + ' "-FileModifyDate<DateTimeOriginal" ' + selected_image
                           args = shlex.split(command_line)
                           p = subprocess.call(args)
        self.progressbar.hide()
        self.lbl_progress.setText("Done writing the info to the selected image(s)")

#------------------------------------------------------------------------

