#!/usr/bin/python

# info_window.py

# Copyright (c) 2011 Harry van der Wolf. All rights reserved.
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

import os, sys, argparse, shlex, subprocess
import PySide
from PySide import QtCore
from PySide.QtGui import QApplication, QMainWindow, QTextEdit, QPushButton,\
                         QWidget, QGridLayout, QTextEdit

# python helper scripts
import programinfo

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
	super(MainWindow, self).__init__(parent)
        self.resize(500, 640)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.info_window_close = QPushButton(self.centralwidget)
        self.info_window_close.setObjectName("info_window_close")
        self.info_window_close.setText("Close")
        self.gridLayout.addWidget(self.info_window_close, 1, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.info_window()
        #self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.info_window_close, QtCore.SIGNAL("clicked()"), self.close)
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("Mainwindow", "image info", None, QApplication.UnicodeUTF8))
        self.license_close.setText(QApplication.translate("Mainwindow", "&Close", None, QApplication.UnicodeUTF8))

    def info_window(self):
        parser = argparse.ArgumentParser(description='Display image info via exiftool or show program information.')
        parser.add_argument('parsed_option', help='Please specify the image with it\'s full path or the license or the about')

	counter = 0
        passed_args = parser.parse_args()
	print "passed_args.parsed_option: " + str(passed_args.parsed_option)
	if passed_args.parsed_option == "about":
		print "asked for about window"
	elif passed_args.parsed_option == "license":
		self.setWindowTitle(programinfo.NAME + " " + programinfo.VERSION + " license")
        	self.textEdit.wordWrapMode()
		self.textEdit.setText(open('COPYING').read())
	else: # image
        	command_line = "exiftool \"" + passed_args.parsed_option + "\""
        	args = shlex.split(command_line)
        	p = subprocess.check_output(args, universal_newlines=True)
		self.setWindowTitle("image info of: " + os.path.basename(passed_args.parsed_option))
        	self.textEdit.wordWrapMode()
        	self.textEdit.setText(p)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())
