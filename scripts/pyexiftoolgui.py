#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyexiftoolgui.py

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

import os, sys, platform, shlex, subprocess, webbrowser, re

import PySide
from PySide.QtCore import *
from PySide.QtGui import *


#-------------------------------------------------------------------------
# Very first check on version
if sys.version_info<(2,7,0):
    sys.stderr.write("\n\nYou need python 2.7 or later to use pyexiftoolgui\n")
    exit(1)
else:
    print("\nProgram start: We are on python " + sys.version)

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
sys.path.append( realfile_dir + "/ui")


# python helper scripts
import petgfunctions
import programinfo
import programstrings
import renaming
import petgfilehandling

#import image_resources.rc
if platform.system() == "Darwin":
    from ui_MainWindowMAC import Ui_MainWindow
else:
    from ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
# Set window title to start with
        self.setWindowTitle(programinfo.NAME + " " + programinfo.VERSION )
# First set the menu actions
        self.mnu_action_load_images.triggered.connect(self.loadimages)
        self.action_Quit.triggered.connect(self.quit_application)
        app.aboutToQuit.connect(self.quit_application)
        #--- Extra menu
        self.mnu_action_modifydatetime.triggered.connect(self.modify_datetime)
        self.mnu_action_create_args.triggered.connect(self.create_args)
        self.mnu_action_export_metadata.triggered.connect(self.export_metadata)
        self.mnu_action_remove_metadata.triggered.connect(self.remove_metadata)
        self.mnu_action_date_to_DateTimeOriginal.triggered.connect(self.date_to_datetimeoriginal)
        self.mnu_action_repair_jpg.triggered.connect(self.repair_jpg_metadata)
        self.mnu_action_copytoxmp.triggered.connect(self.copymetadatatoxmp)
        self.mnu_action_renaming.triggered.connect(self.rename_photos)
        #self.mnu_action_define_lens.triggered.connect(self.lensdialog)
        #self.menuExtra.removeAction(self.mnu_action_renaming)
        #--- help menu
        self.mnu_action_pyexiftoolgui_home.triggered.connect(self.open_pyexiftoolgui_homepage)
        self.mnu_action_exiftool.triggered.connect(self.open_exiftool_homepage)
        self.mnu_action_manual.triggered.connect(self.open_manual)
        #self.mnu_action_mapcoordinates_tab.triggered.connect(self.mapcoordinates_help)
        self.mnu_action_license.triggered.connect(self.show_license)
        self.mnu_action_Donate.triggered.connect(self.open_donate_page)
        self.mnu_action_Info.triggered.connect(self.show_about_window)
        # Set extra actions for context menu (others taken from normal menu)
        self.imagereference = QAction("Select photo as reference for \"Extra\" menu", self, triggered = self.reference_image)
        self.displayphoto = QAction("Display selected photo", self, triggered = self.showimage)
# Load several views, buttons, comboboxes, spinboxes and labels from main screen
        self.btn_loadimages.clicked.connect(self.loadimages)
        self.showimagebutton.clicked.connect(self.showimage)
        self.showimagebutton.setEnabled(False)
        self.statusbar.showMessage("")
        self.progressbar.hide()
        self.comboBox_languages.currentIndexChanged.connect(self.comboBox_languageschanged)
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
# Load several buttons from the Edit -> Geotagging tab
        self.btn_geotagging_help.clicked.connect(self.geotagging_help)
        self.btn_geotag_img_browse.clicked.connect(self.geotag_source_folder)
        self.btn_geotag_gps_track_browse.clicked.connect(self.geotag_gps_file)
        self.btn_write_geotaginfo.clicked.connect(self.write_geotag_info)
        self.btn_write_geotaginfo.setEnabled(False)
# Load several buttons from the Edit -> lens tab
        self.chk_predefined_lenses.clicked.connect(self.check_self_defined_lenses)
        self.btn_lenshelp.clicked.connect(self.lens_help)
        self.btn_lens_copyfrom.clicked.connect(self.copylensfromselected)
        self.btn_lens_copyfrom.setEnabled(False)
        self.btn_savelens.clicked.connect(self.savelensdata)
        self.btn_savelens.setEnabled(False)
        self.btn_resetlens.clicked.connect(self.clear_lens_fields)
        self.btn_save_lens.clicked.connect(self.savelens)
        self.btn_update_lens.clicked.connect(self.updatelens)
        self.btn_delete_lens.clicked.connect(self.deletelens)
        self.predefined_lenses.currentIndexChanged.connect(self.definedlenschanged)
        # For the time being hide the button
        #self.btn_copy_lens_defaults.setVisible(False)
# Load several buttons from the Edit -> Your commands tab
        self.btn_yourcommands_clearinput.clicked.connect(self.clear_yourcommands_input)
        self.btn_yourcommands_clearoutput.clicked.connect(self.clear_yourcommands_output)
        self.btn_yourcommands_go.clicked.connect(self.yourcommands_go)
        self.btn_yourcommands_help.clicked.connect(self.yourcommands_help)
# Load several buttons from the Preferences tab
        self.btn_preferences_save.clicked.connect(self.preferences_save)
        self.btn_preferenceshelp.clicked.connect(self.preferences_help)
        self.btn_choose_exiftool.clicked.connect(self.select_exiftool)
        self.btn_choose_defstartupfolder.clicked.connect(self.select_defstartupfolder)


#------------------------------------------------------------------------
# Define a few globals and variables
        self.DebugMsg = False
        self.allDebugMsg = False
        self.logging = ""
        self.logtofile = 0
#         self.tmpworkdir = tempfile.gettempdir() +"/pyGPSTtmp"

        self.OSplatform = platform.system()
        #petgfunctions.read_config(self)
        petgfilehandling.read_xml_config(self)
        # First clean up and recreate our temporary workspace
#        petgfunctions.remove_workspace( self )
#        try:
#        fldr = os.mkdir(self.tmpworkdir)
#        except:
#        if self.logtofile:
#            logging.info(self.tmpworkdir + " already exists.")

#------------------------------------------------------------------------
# Initialize file paths
        self.realfile_dir  = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir    = os.path.dirname(self.realfile_dir)
        self.ui_dir    = os.path.join(self.realfile_dir, "ui")

#------------------------------------------------------------------------
# Start up functions
#        OSplatform, img_converter, enfuseprg, aisprg = petgfunctions.startup_checks(self)
#            self.OSplatform = OSplatform
#         if self.allDebugMsg:
#             ret = QMessageBox.about(self, "returned check values",
#                                      "platform: %s\nconverter: %s\nenfuse: %s\nais: %s"
#                                       % (OSplatform, img_converter, enfuseprg, aisprg))

        # Startup check for available tools
        self.exiftoolversion = "0.00"
        petgfunctions.tool_check(self)
        # Now that we know that we have exiftool version and languages available split the languages
        petgfunctions.exitool_languages(self)

        # Initialize Combobox on lens tab with loaded lenses (if any)
        self.lens_current_index = ''  # We need this later when updating or deleting lenses
        petgfilehandling.read_defined_lenses(self, qApp)

        # Initialize Combobox mass change tab
        '''self.grouplist = [
        self.tr('exif'),
        self.tr('jfif'),
        self.tr('gps'),
        self.tr('iptc'),
        self.tr('xmp'),
        self.tr('icc_profile'),
        self.tr('makernotes'),
        ] '''

#------------------------------------------------------------------------
# General functions
    def quit_application(self):
        #petgfunctions.remove_workspace(self)
        petgfilehandling.write_xml_config(self)
        self.close()

#    def set_logging(self):
#        logging.basicConfig(filename=os.path.expanduser("~/pyexiftoolgui_"+time.strftime("%Y%m%d-%H%M%S")+".log"),level=logging.DEBUG)
#        logging.info("Debug set to on: Logging started on " + time.strftime("%Y-%m-%d %H:%M"))
    def the_no_photos_messagebox(self):
        QMessageBox.information(self,"No photos loaded yet","You did not load or select any photos yet.")

#     def testfunc(self):
#         ret = petgfunctions.startup_checks(self)

    def enableimagebuttons(self):
        self.showimagebutton.setEnabled(True)
        self.imageinfobutton.setEnabled(True)


    def loadimages(self):
        ''' show dialog of image files and load images selected '''
        selectedimages = petgfunctions.images_dialog(self, qApp)
        petgfunctions.loadimages(self, selectedimages, qApp)
        # If we alread did some copying or simply working on the GPS:edit tab we need to clean it after loading new images
        #petgfunctions.clear_gps_fields(self)


    def load_cmd_images(self, args):
        ''' load images from command line args'''
        petgfunctions.loadimages(self, args, qApp)

    def comboBox_languageschanged(self):
        petgfunctions.comboBox_languageschanged(self)

    def activate_buttons_events(self):
        # enable buttons that can only work once we have images loaded
        self.showimagebutton.setEnabled(True)
        self.btn_gps_copyfrom.setEnabled(True)
        self.btn_savegps.setEnabled(True)
        self.btn_exif_copyfrom.setEnabled(True)
        self.btn_saveexif.setEnabled(True)
        if float(self.exiftoolversion) > 9.06:
            self.btn_gpano_copyfrom.setEnabled(True)
            self.btn_savegpano.setEnabled(True)
        self.btn_xmp_copyfrom.setEnabled(True)
        self.btn_savexmp.setEnabled(True)
        self.btn_write_geotaginfo.setEnabled(True)
        self.btn_lens_copyfrom.setEnabled(True)
        self.btn_savelens.setEnabled(True)
        self.progressbar.hide()
        self.statusbar.showMessage("Click thumb or filename to display the image info")
        # Set proper events
        self.MaintableWidget.cellClicked.connect(self.imageinfo)
        self.radioButton_all.clicked.connect(self.imageinfo)
        self.radioButton_exif.clicked.connect(self.imageinfo)
        self.radioButton_xmp.clicked.connect(self.imageinfo)
        self.radioButton_iptc.clicked.connect(self.imageinfo)
        self.radioButton_gps.clicked.connect(self.imageinfo)
        self.radioButton_gpano.clicked.connect(self.imageinfo)
        self.radioButton_iccprofile.clicked.connect(self.imageinfo)
        self.radioButton_makernotes.clicked.connect(self.imageinfo)

#------------------------------------------------------------------------
# Context menu
    def contextMenuEvent(self, event):
        cntxtmenu = ""
        cntxtmenu = QMenu(self)
        try:
            if len(self.fileNames) > 0:
                cntxtmenu.addAction(self.mnu_action_load_images)
                cntxtmenu.addAction(self.mnu_action_renaming)
                cntxtmenu.addAction(self.imagereference)
                cntxtmenu.addAction(self.displayphoto)
                cntxtmenu.addAction(self.mnu_action_create_args)
                cntxtmenu.addAction(self.mnu_action_export_metadata)
                cntxtmenu.addAction(self.mnu_action_modifydatetime)
                cntxtmenu.addAction(self.mnu_action_date_to_DateTimeOriginal)
                cntxtmenu.addAction(self.mnu_action_repair_jpg)
                cntxtmenu.addAction(self.mnu_action_remove_metadata)
        except:
            # no images loaded yet
            cntxtmenu.addAction(self.mnu_action_load_images)
            cntxtmenu.addAction(self.mnu_action_renaming)
            cntxtmenu.addAction(self.mnu_action_Info)
            cntxtmenu.addAction(self.mnu_action_license)
        cntxtmenu.exec_(event.globalPos())

    def reference_image(self):
        selected_row = self.MaintableWidget.currentRow()
        self.referenceimage = "\"" + self.fileNames[selected_row] + "\""
        print(str(self.referenceimage))

#------------------------------------------------------------------------
# Menu actions/functions
    def show_about_window(self):
        self.aboutbox = QMessageBox()

        self.licenselabel = QLabel()
        self.licensebutton = self.aboutbox.addButton(self.tr("License"), QMessageBox.ActionRole)
        self.donatelabel = QLabel()
        self.donatebutton = self.aboutbox.addButton(self.tr("Donate"), QMessageBox.ActionRole)

        closebutton = self.aboutbox.addButton(QMessageBox.Close)

        self.licensebutton.clicked.connect(self.show_license)
        self.donatebutton.clicked.connect(self.open_donate_page)
        self.aboutbox.setWindowTitle("About pyexiftoolgui " + programinfo.VERSION)
        if platform.system() == "Darwin":
            self.aboutbox.setText("<p>This is<b> " + programinfo.NAME + " " + programinfo.VERSION + "</b></p>" + programinfo.ABOUTMESSAGE)
        else:
            self.aboutbox.setText(programinfo.ABOUTMESSAGE)

        ret = self.aboutbox.exec_()

    def show_license(self):
        petgfunctions.info_window(self)

    def rename_photos(self):
        renaming.rename_photos(self,qApp)

    def create_args(self):
        try:
            if len(self.fileNames) == 0:
                self.the_no_photos_messagebox()
            else:
                petgfunctions.create_args(self, qApp)
        except:
            self.the_no_photos_messagebox()

    def export_metadata(self):
        try:
            if len(self.fileNames) == 0:
                self.the_no_photos_messagebox()
            else:
                petgfunctions.export_metadata(self, qApp)
        except:
            self.the_no_photos_messagebox()

    def remove_metadata(self):
        try:
            if len(self.fileNames) == 0:
                self.the_no_photos_messagebox()
            else:
                petgfunctions.remove_metadata(self, qApp)
        except:
            self.the_no_photos_messagebox()


    def modify_datetime(self):
        try:
            if len(self.fileNames) == 0:
                self.the_no_photos_messagebox()
            else:
                petgfunctions.modifydatetime(self, qApp)
        except:
            self.the_no_photos_messagebox()

    def date_to_datetimeoriginal(self):
        try:
            if len(self.fileNames) == 0:
                self.the_no_photos_messagebox()
            else:
                petgfunctions.date_to_datetimeoriginal(self, qApp)
        except:
            self.the_no_photos_messagebox()

    def open_pyexiftoolgui_homepage(self):
        try:
            webbrowser.open("http://hvdwolf.github.io/pyExifToolGUI/")
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


    def repair_jpg_metadata(self):
        et_param = "-all= -tagsfromfile @ -all:all -unsafe -F "
        message = "If exiftool can't write to your photo it might be due to corrupted metadata. Exiftool can fix this but only "
        message += "for the tags that are still readible. In a jpeg the image data is separated from the meta data. If your "
        message += "photo can't be displayed in an image viewer, your image data itself is corrupt. Exiftool can't repair that.\n\n"
        message += "Do you want to continue and repair as much metadata as possible?"
        reply = QMessageBox.question(self, "Repair corrupted metadata in JPG(s)", message, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Add true to write function: Always make a backup in this case
            petgfunctions.write_image_info(self, et_param, qApp, True)

    def copymetadatatoxmp(self):
        et_param = "copymetadatatoxmp"
        message = "This function will copy all possible information from exif and other tags into XMP format.\n"
        message += "This is an internal \"same image to same image\" copy, for all the selected images.\n\n"
        message += "Do you want to continue?"
        reply = QMessageBox.question(self, "Copy all metadata to xmp format?", message, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            petgfunctions.write_image_info(self, et_param, qApp, False)

#------------------------------------------------------------------------
# Help functions leading to html manual
    def all_access_to_manual(self, section):
        if section != "":
            section = "#" + section
        manual = "pyexiftoolgui.html" + section
        try:
            if self.OSplatform == "Windows":
                if os.path.isfile(os.path.join(self.realfile_dir, "manual","pyexiftoolgui.html")): # from python executable
                    webbrowser.open(os.path.join(self.realfile_dir, "manual",manual))
                elif os.path.isfile(os.path.join(self.parent_dir, "manual","pyexiftoolgui.html")): # Started from script
                    webbrowser.open(os.path.join(self.parent_dir, "manual",manual))
            elif self.OSplatform == "Darwin":
                if os.path.isfile(os.path.join(self.realfile_dir, "pyexiftoolgui.app","Contents","MacOS","manual","pyexiftoolgui.html")): # from python app
                    webbrowser.open("file://" + os.path.join(self.realfile_dir, "pyexiftoolgui.app","Contents","MacOS","manual", manual))
                elif os.path.isfile(os.path.join(self.parent_dir, "manual","pyexiftoolgui.html")): # Started from script
                    webbrowser.open("file://" + os.path.join(self.parent_dir, "manual" , manual))
            else:
                webbrowser.open("file://" + os.path.join(self.parent_dir, "manual", manual))
        except:
            QMessageBox.critical(self, "Error!", "Unable to open the manual" )

    def open_manual(self):
        self.all_access_to_manual("")

    def gps_help(self):
        self.all_access_to_manual("EditgpsData")

    def exif_help(self):
        self.all_access_to_manual("EditexifData")

    def xmp_help(self):
        self.all_access_to_manual("EditxmpData")

    def gpano_help(self):
        self.all_access_to_manual("EditgpanoData")

    def geotagging_help(self):
        self.all_access_to_manual("Geotagging")

    def lens_help(self):
        self.all_access_to_manual("EditlensData")

    def yourcommands_help(self):
        self.all_access_to_manual("YourCommands")

    def preferences_help(self):
        self.all_access_to_manual("Preferences")

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

# Edit -> Geotagging tab
    def geotag_source_folder(self):
        petgfunctions.geotag_source_folder(self, qApp)
#---
    def geotag_gps_file(self):
        petgfunctions.geotag_gps_file(self, qApp)
#---
    def write_geotag_info(self):
            print("pushed button to write the geotag info")
            self.statusbar.showMessage("writing geotag information to image(s).")
            petgfunctions.write_geotag_info(self,qApp)

# Edit -> lens tab
    def check_self_defined_lenses(self):
        petgfunctions.check_self_defined_lenses(self)

    def clear_lens_fields(self):
        petgfunctions.clear_lens_fields(self)

    def copylensfromselected(self):
        petgfunctions.copylensfromselected(self,qApp)

    def lens_defaults(self):
        petgfunctions.copy_defaults(self, qApp, "lens")

    def savelensdata(self): # save data to image
        petgfunctions.savelensdata(self, qApp)

    def savelens(self): # save lens data to lens db
        petgfilehandling.savelens(self, qApp)

    def updatelens(self):
        petgfunctions.updatelens(self, qApp)

    def deletelens(self):
        petgfunctions.clear_lens_fields(self)
        petgfilehandling.deletelens(self, qApp)

    def definedlenschanged(self):
        petgfunctions.definedlenschanged(self, qApp)

# Your Commands tab
    def clear_yourcommands_input(self):
        self.yourcommands_input.setText("")

    def clear_yourcommands_output(self):
        #self.yourcommands_output.insertPlainText("")
        self.yourcommands_output.clear()

    def yourcommands_go(self):
        self.yourcommands_output.clear()
        petgfunctions.yourcommands_go(self,qApp)

# Preferences tab
    def select_exiftool(self):
        select_exiftool = QFileDialog(self)
        qApp.processEvents()
        select_exiftool.setFileMode(QFileDialog.ExistingFile)
        select_exiftool.setViewMode(QFileDialog.Detail)
        select_exiftool.setFilters(["exiftool.exe", "*.exe"])
        if select_exiftool.exec_():
            files_list = select_exiftool.selectedFiles()
            print("files_list[0]" + str(files_list[0]))
            self.exiftooloption.setText(files_list[0])
            return files_list[0]
        else:
            # user canceled
            self.statusbar.showMessage("you canceled the exiftool selection.")
            return ""

    def select_defstartupfolder(self):
        select_defstartupfolder = QFileDialog(self)
        qApp.processEvents()
        select_defstartupfolder.setFileMode(QFileDialog.Directory)
        select_defstartupfolder.setViewMode(QFileDialog.Detail)
        if select_defstartupfolder.exec_():
            self.defstartupfolder = select_defstartupfolder.selectedFiles()[0]
            self.LineEdit_def_startupfolder.setText(self.defstartupfolder)
            print(str(self.defstartupfolder))
        else:
            # user canceled
            self.statusbar.showMessage("you canceled the default image startup folder selection.")
            self.defstartupfolder = ""

    def preferences_save(self):
        petgfilehandling.write_xml_config(self)
        petgfunctions.tool_check(self)


#------------------------------------------------------------------------
# This is where we define some "empty" functions called from another script
# which need to be "self enabled". These are for the new dialogs.
    def check_create_args_boxes(self):
        petgfunctions.check_create_args_boxes(self)

    def check_xmpexport_metadata_boxes(self):
        petgfunctions.check_xmpexport_metadata_boxes(self)

    def check_export_metadata_boxes(self):
        petgfunctions.check_export_metadata_boxes(self)

    def check_remove_metadata_boxes(self):
        petgfunctions.check_remove_metadata_boxes(self)

    def moddialog_shift_clicked(self):
        petgfunctions.qddt_shift_clicked(self)

    def moddialog_use_reference_image_data(self):
        petgfunctions.qddt_use_reference_image_data(self)

    def check_radiobuttons(self):
        renaming.check_radiobuttons(self)

#------------------------------------------------------------------------
#------------------------------------------------------------------------
# This is where the main app is started

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()

    if len(sys.argv) > 1:
        print('Number of arguments: %d' % len(sys.argv))
        print('Argument List:' + str(sys.argv))
        frame.load_cmd_images(sys.argv[1:])

    app.exec_()
