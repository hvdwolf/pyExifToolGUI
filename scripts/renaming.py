# -*- coding: utf-8 -*-

# renaming.py - This python "helper" script holds the renaming and restructuring functions

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

import PySide
from PySide.QtCore import *
from PySide.QtGui import *
#from PySide.QtUiTools import *

import programstrings
import petgfunctions

from ui_rename_photos import Ui_Dialog_rename_files

#------------------------------------------------------------------------
#--- All renaming functions

class dialog_rename_photos(QDialog, Ui_Dialog_rename_files):
    # This loads the py file created by pyside-uic from the ui.
    # the Quiloader segfaults on windows after ending the function
    def __init__(self, parent=None):
        super(dialog_rename_photos, self).__init__(parent)
        self.setupUi(self)
        # initialize buttons
        self.button_rename_info.clicked.connect(self.rename_info)
        self.button_rename_browse.clicked.connect(self.source_folder)
        # disable date/time suffix options as program stats wth datetime prefix as default
        self.radioButton_suffix_datetime.setEnabled(False)
        self.radioButton_suffix_date.setEnabled(False)
        self.comboBox_suffix_datetime.setEnabled(False)
        self.comboBox_suffix_date.setEnabled(False)
        self.tabWidget.removeTab(1)


    def rename_info(self):
        message = "If you leave the \"source folder\" empty, the program will use the selected photos from the main screen.\n"
        message += "If you specify a source folder in this screen, this screen will use all content inside that folder.\n\n"
        message += "Note that working on a directory instead of a collection of files is about 10! times as fast.\n\n"
        message += "You can on the other hand load an extensive set of photos in the main screen and update subselections of them in two or three rounds."
        QMessageBox.information(self,"folder options", message)


    def source_folder(self):
        select_folder = QFileDialog(self)
        select_folder.setFileMode(QFileDialog.Directory)
        if platform.system() == "Darwin":
            select_folder.setDirectory(os.path.expanduser('~/Pictures'))
        elif platform.system() == "Linux":
            select_folder.setDirectory(os.path.expanduser('~/Pictures'))
        elif platform.system() == "Windows":
            select_folder.setDirectory(os.path.expanduser('~/My Pictures'))
        select_folder.setViewMode(QFileDialog.Detail)
        self.rename_source_folder = ""
        if select_folder.exec_():
            self.rename_source_folder = select_folder.selectedFiles()[0]
            self.LineEdit_rename_source_folder.setText(self.rename_source_folder)
            print(str(self.rename_source_folder))
        else:
            # user canceled
            self.statusbar.showMessage("you canceled selecting a folder for the renaming options.")
            self.rename_source_folder = ""
#---
def check_radiobuttons(self):
    if (self.rename_photos_dialog.radioButton_prefix_datetime.isChecked()) or (self.rename_photos_dialog.radioButton_prefix_date.isChecked()):
        self.rename_photos_dialog.radioButton_suffix_datetime.setEnabled(False)
        self.rename_photos_dialog.radioButton_suffix_date.setEnabled(False)
        self.rename_photos_dialog.comboBox_suffix_datetime.setEnabled(False)
        self.rename_photos_dialog.comboBox_suffix_date.setEnabled(False)
        self.rename_photos_dialog.radioButton_suffix_donotuse.setChecked(1)
        self.rename_photos_dialog.radioButton_suffix_donotuse.setEnabled(True)
        self.rename_photos_dialog.suffix_string.setEnabled(True)
        self.rename_photos_dialog.radioButton_suffix_string.setEnabled(True)
    elif self.rename_photos_dialog.radioButton_prefix_string.isChecked():
        self.rename_photos_dialog.radioButton_suffix_donotuse.setEnabled(False)
        self.rename_photos_dialog.radioButton_suffix_string.setEnabled(False)
        self.rename_photos_dialog.suffix_string.setEnabled(False)
        self.rename_photos_dialog.suffix_string.setText("")
        self.rename_photos_dialog.radioButton_suffix_datetime.setEnabled(True)
        self.rename_photos_dialog.comboBox_suffix_datetime.setEnabled(True)
        self.rename_photos_dialog.comboBox_suffix_date.setEnabled(True)
        self.rename_photos_dialog.radioButton_suffix_datetime.setChecked(1)
        self.rename_photos_dialog.radioButton_suffix_date.setEnabled(True)

#---
def rename_photos(self, qApp):
    self.rename_photos_dialog = dialog_rename_photos()
    # initialize radiobutton events
    self.rename_photos_dialog.radioButton_prefix_datetime.clicked.connect(self.check_radiobuttons)
    self.rename_photos_dialog.radioButton_prefix_date.clicked.connect(self.check_radiobuttons)
    self.rename_photos_dialog.radioButton_prefix_string.clicked.connect(self.check_radiobuttons)


    if self.rename_photos_dialog.exec_() == QDialog.Accepted:
        # First check if we have something to work on
        result = check_before_run_rename_photos(self)
        if result == "nothing_to_work_with":
            # error message already displayed, exit function
            return
        else:
            work_on = result
            # analyze prefix
            self.fulldatetime = False
            self.prefix = "${CreateDate}"
            if self.rename_photos_dialog.radioButton_prefix_datetime.isChecked():
                if self.rename_photos_dialog.comboBox_prefix_datetime.currentText() == "YYYYMMDDHHMMSS":
                    prefix_message = "YYYYMMDDHHMMSS"
                    self.prefixformat = "-d %Y%m%d%H%M%S"
                    self.fulldatetime = True
                elif self.rename_photos_dialog.comboBox_prefix_datetime.currentText() == "YYYYMMDD_HHMMSS":
                    prefix_message = "YYYYMMDD_HHMMSS"
                    self.prefixformat = "-d %Y%m%d_%H%M%S"
                    self.fulldatetime = True
                elif self.rename_photos_dialog.comboBox_prefix_datetime.currentText() == "YYYMMDD-HHMMSS":
                    prefix_message = "YYYMMDD-HHMMSS"
                    self.prefixformat = "-d %Y%m%d-%H%M%S"
                    self.fulldatetime = True
                elif self.rename_photos_dialog.comboBox_prefix_datetime.currentText() == "YYYY_MM_DD_HH_MM_SS":
                    prefix_message = "YYYY_MM_DD_HH_MM_SS"
                    self.prefixformat = "-d %Y_%m_%d_%H_%M_%S"
                    self.fulldatetime = True
                elif self.rename_photos_dialog.comboBox_prefix_datetime.currentText() == "YYYY-MM-DD-HH-MM-SS":
                    prefix_message = "YYYY-MM-DD-HH-MM-SS"
                    self.prefixformat = "-d %Y-%m-%d-%H-%M-%S"
                    self.fulldatetime = True
            elif self.rename_photos_dialog.radioButton_prefix_date.isChecked():
                if self.rename_photos_dialog.comboBox_prefix_date.currentText() == "YYYYMMDD":
                    prefix_message = "YYYYMMDD"
                    self.prefixformat = " -d %Y%m%d"
                elif self.rename_photos_dialog.comboBox_prefix_date.currentText() == "YYYY_MM_DD":
                    prefix_message = "YYYY_MM_DD"
                    self.prefixformat = "-d %Y_%m_%d"
                elif self.rename_photos_dialog.comboBox_prefix_date.currentText() == "YYYY-MM-DD":
                    prefix_message = "YYYY-MM-DD"
                    self.prefixformat = "-d %Y-%m-%d"
            elif self.rename_photos_dialog.radioButton_prefix_string.isChecked():
                prefix_message = self.rename_photos_dialog.prefix_string.text()
                self.prefix = self.rename_photos_dialog.prefix_string.text()
                self.prefixformat = ""
            # analyze suffix
            self.suffix = "${CreateDate}"
            if self.rename_photos_dialog.radioButton_suffix_donotuse.isChecked():
                self.suffix = ""
                self.suffixformat = ""
            else:
                if self.rename_photos_dialog.radioButton_suffix_string.isChecked():
                    suffix_message = self.rename_photos_dialog.suffix_string.text()
                    self.suffix = self.rename_photos_dialog.suffix_string.text()
                    self.suffixformat = ""
                elif self.rename_photos_dialog.radioButton_suffix_datetime.isChecked():
                    if self.rename_photos_dialog.comboBox_suffix_datetime.currentText() == "YYYYMMDDHHMMSS":
                        suffix_message = "YYYYMMDDHHMMSS"
                        self.suffixformat = "-d %Y%m%d%H%M%S"
                        self.fulldatetime = True
                    elif self.rename_photos_dialog.comboBox_suffix_datetime.currentText() == "YYYYMMDD_HHMMSS":
                        suffix_message = "YYYYMMDD_HHMMSS"
                        self.suffixformat = "-d %Y%m%d_%H%M%S"
                        self.fulldatetime = True
                    elif self.rename_photos_dialog.comboBox_suffix_datetime.currentText() == "YYYMMDD-HHMMSS":
                        suffix_message = "YYYMMDD-HHMMSS"
                        self.suffixformat = "-d %Y%m%d-%H%M%S"
                        self.fulldatetime = True
                    elif self.rename_photos_dialog.comboBox_suffix_datetime.currentText() == "YYYY_MM_DD_HH_MM_SS":
                        suffix_message = "YYYY_MM_DD_HH_MM_SS"
                        self.suffixformat = "-d %Y_%m_%d_%H_%M_%S"
                        self.fulldatetime = True
                    elif self.rename_photos_dialog.comboBox_suffix_datetime.currentText() == "YYYY-MM-DD-HH-MM-SS":
                        suffix_message = "YYYY-MM-DD-HH-MM-SS"
                        self.suffixformat = "-d %Y-%m-%d-%H-%M-%S"
                        self.fulldatetime = True
                elif self.rename_photos_dialog.radioButton_suffix_date.isChecked():
                    if self.rename_photos_dialog.comboBox_suffix_date.currentText() == "YYYYMMDD":
                        suffix_message = "YYYYMMDD"
                        self.suffixformat = "-d %Y%m%d"
                    elif self.rename_photos_dialog.comboBox_suffix_date.currentText() == "YYYY_MM_DD":
                        suffix_message = "YYYY_MM_DD"
                        self.suffixformat = "-d %Y_%m_%d"
                    elif self.rename_photos_dialog.comboBox_suffix_date.currentText() == "YYYY-MM-DD":
                        suffix_message = "YYYY-MM-DD"
                        self.suffixformat = "-d %Y-%m-%d"
                elif self.rename_photos_dialog.radioButton_model.isChecked():
                    self.suffix = "${Exif:Model}"
                    suffix_message = "${Exif:Model}"
                    self.suffixformat = ""
                elif self.rename_photos_dialog.radioButton_orgfilename.isChecked():
                    self.suffix = "${filename}"
                    suffix_message = "${filename}"
                    self.suffixformat = ""

        # how does the user wants his/her extension
        if self.rename_photos_dialog.radioButton_fileext_asis.isChecked():
            self.rename_extension = ".%e"
        elif self.rename_photos_dialog.radioButton_fileext_tolower.isChecked():
            self.rename_extension = ".%le"
        else:
            self.rename_extension = ".%ue"
        # Does the user want to start counting as of the first image or starting on the second image
        if self.rename_photos_dialog.comboBox_startcount.currentIndex() == 0:
            self.startcounting = "nc"
            print("start counting on 1st image")
        else:
            self.startcounting = "c"
            print("start counting on 2nd image")

        message = "You selected:\n\n"
        message += prefix_message
        if self.rename_photos_dialog.radioButton_suffix_string.isChecked():
            message += "_" + suffix_message

        #QMessageBox.information(self,"Renaming photos", message)
        run_rename_photos(self, work_on, qApp)
    else:
        print("you cancelled") 
        self.statusbar.showMessage("you canceled the \"Rename photos\" action")
#---
def check_before_run_rename_photos(self):
    print("self.rename_photos_dialog.LineEdit_rename_source_folder #" + self.rename_photos_dialog.LineEdit_rename_source_folder.text() + "#")
    if self.rename_photos_dialog.LineEdit_rename_source_folder.text() == "":
        # user did not select a source folder, now check in the except whether he/she selected images in the main screen
        try:
            #if len(self.fileNames) == 0:
            selected_rows = self.MaintableWidget.selectedIndexes()
            if len(selected_rows) == 0:
                QMessageBox.information(self,"Nothing to work with","You did not specify a source folder and neither did you load/select any photos in the main screen.")
                return "nothing_to_work_with"
            else:
                # just exit this function with the option "main_screen_selection"
                print("main_screen_selection")
                return "main_screen_selection"
        except:
            QMessageBox.information(self,"Nothing to work with","You did not specify a source folder and neither did you load/select any photos in the main screen.")
            return "nothing_to_work_with"
    else:
        # just exit this function with the option rename_source_folder (this is not the path)
        print("rename_source_folder")
        return "rename_source_folder"
#---
def run_rename_photos(self, work_on, qApp):
    '''
    Examples
    D:/Datadir/python/exiftool.exe "-FileName<${CreateDate}_pipo%-.3nc.%e"  -d %Y%m%d "D:\Datadir\fototest\testje"
    20121114_pipo-001.jpg
    20121114_pipo-002.jpg
    20121114_pipo-003.jpg
    20121114_pipo-004.jpg

    D:/Datadir/python/exiftool.exe "-FileName<${CreateDate}_pipo.%e"  -d %Y%m%d%%-.3nc "D:\Datadir\fototest\testje"
    20121114-001_pipo.jpg
    20121114-002_pipo.jpg
    20121114-003_pipo.jpg
    20121114-004_pipo.jpg

    D:/Datadir/python/exiftool.exe "-FileName<pipo_${Exif:Model}%-.2c.%e" "D:\Datadir\fototest\testje"
    pipo_DMC-TZ30-00.jpg
    pipo_DMC-TZ30-01.jpg
    pipo_DMC-TZ30-02.jpg
    pipo_DMC-TZ30-03.jpg

    D:/Datadir/python/exiftool.exe "-FileName<pipo_${CreateDate}%-.2nc.%e" -d %Y%m%d "D:\Datadir\fototest\testje"
    pipo_20121114-01.jpg
    pipo_20121114-02.jpg
    pipo_20121114-03.jpg
    pipo_20121114-04.jpg

    D:/Datadir/python/exiftool.exe "-FileName<pipo_${Exif:Model}.%e" -d%%-.2c "D:\Datadir\fototest\testje"
    does not work!
    '''
    # build our exiftoolparams string
    # exiftoolparams = "'-FileName<" + self.prefix + "_" + self.suffix + ".%le' " + self.prefixformat + " " + self.suffixformat + "-." + self.combobox_digits.currenttext() + "nc" + self.sourcefolder + "/*"
    exiftoolparams = "'-FileName<" + self.prefix
    if not self.rename_photos_dialog.radioButton_suffix_donotuse.isChecked():
        exiftoolparams += "_" + self.suffix
    print("self.fulldatetime " + str(self.fulldatetime))
    if self.fulldatetime == True: 
        # This means that the autonumber should only work on images that have the same full datetime
        exiftoolparams += "%-" + self.rename_photos_dialog.comboBox_digits.currentText() + self.startcounting
    else:
        exiftoolparams += "%-." + self.rename_photos_dialog.comboBox_digits.currentText() + self.startcounting
    print("numbering: exiftoolparams " + exiftoolparams)
    # Do everything split for a prefix as date(time) vs. string; no combined actions, is much simpler       
    if self.prefixformat != "":
        # This means that the prefix is a date(time)
        exiftoolparams += self.rename_extension + "' " + self.prefixformat
        # both lines above mean : prefix_suffix_number.extension
    else:
        # this means that we use a string instead of date(time) as prefix
        # if self.prefixformat is empty we need to move the "counter"
        exiftoolparams += self.rename_extension + "'"
        if self.suffixformat != "":
            exiftoolparams += " " + self.suffixformat

    # now start working and detect which images we use
    if work_on == "nothing_to_work_with":
        # This should already have been dealt with earlier, but in case I did something stupid we simply exit this function
        return
    elif work_on == "main_screen_selection":
        # we use the images that were selected from the main screen
        print("we use the images that were selected from the main screen")
        selected_rows = self.MaintableWidget.selectedIndexes()
        #exiftoolparams = "'-FileName<" + self.prefix + "_" + self.suffix + ".%le' " + self.prefixformat + " " + self.suffixformat + "-." + self.combobox_digits.currenttext() + "nc" + self.sourcefolder + "/*"
        rowcounter = 0
        total_rows = len(selected_rows)
        self.progressbar.setRange(0, total_rows)
        self.progressbar.setValue(0)
        self.progressbar.show()
        rows = []
        selected_images = ""
        message_images = ""
        qApp.processEvents()
        for selected_row in selected_rows:
            selected_row = str(selected_row)
            selected_row = selected_row.replace("<PySide.QtCore.QModelIndex(",'')
            selected_row, tail = re.split(',0x0',selected_row)
            #print str(selected_row)
            row, column = re.split(',',selected_row)
            if row not in rows:
                rows.append(row)
                selected_image = "\"" + self.fileNames[int(row)] + "\""
                selected_images += " " + selected_image + " "
                message_images += " " + os.path.basename(selected_image) + " "
                self.progressbar.setValue(rowcounter)
                #   p = subprocess.call(args)
        parameters = ' -fileorder datetimeoriginal# ' + exiftoolparams + ' ' + selected_images
        print('parameters ' + parameters)
        self.statusbar.showMessage("Renaming " + message_images)
        qApp.processEvents()
        if self.OSplatform in ("Windows", "win32"):
            parameters = parameters.replace("/", "\\")
            parameters = parameters.replace("'", "\"")
            args = '"' + self.exiftoolprog + '" ' + parameters
            print(args)
            p = subprocess.call(args, shell=True)
        else:
            #parameters = parameters.replace("'", "\"")
            command_line = self.exiftoolprog + ' -fileorder datetimeoriginal# ' + exiftoolparams + ' ' + selected_images
            args = shlex.split(command_line)
            print("command_line " + command_line)
            #p = subprocess.call(command_line)
            p = subprocess.call(args)
        self.statusbar.showMessage("Finished renaming")
        qApp.processEvents()
        self.progressbar.hide()
        self.statusbar.showMessage("")
    elif work_on == "rename_source_folder":
        # work on all images in the source folder and do it in this function self
        #print "work on all images in the source folder"
        #print self.rename_photos_dialog.LineEdit_rename_source_folder.text()
        self.statusbar.showMessage("Renaming all images in: " + self.rename_photos_dialog.LineEdit_rename_source_folder.text())
        parameters = ' -fileorder datetimeoriginal# ' + exiftoolparams + ' "' + self.rename_photos_dialog.LineEdit_rename_source_folder.text() + '"'
        if self.OSplatform in ("Windows", "win32"):
            parameters = parameters.replace("/", "\\")
            parameters = parameters.replace("'", "\"")
            args = '"' + self.exiftoolprog + '" ' + parameters
            print(args)
            p = subprocess.call(args, shell=True)
        else:
            pathofimages = self.rename_photos_dialog.LineEdit_rename_source_folder.text().replace(" ", "\\ ")
            command_line = self.exiftoolprog + ' ' + exiftoolparams + ' ' + pathofimages
            #print "command_line " + command_line
            p = subprocess.call(command_line, shell=True)
        self.statusbar.showMessage("Finished renaming all images in: " + self.rename_photos_dialog.LineEdit_rename_source_folder.text())
    # Now continue with our renaming stuff
    #QMessageBox.information(self,"selected options", "self.prefix: " + self.prefix + " self.prefixformat: " + self.prefixformat + "\nself.suffix: " + self.suffix + " self.suffixformat: " + self.suffixformat + "\n\n\n" + exiftoolparams)

