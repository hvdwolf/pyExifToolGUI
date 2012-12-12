# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'remove_metadata.ui'
#
# Created: Wed Dec 12 13:28:52 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog_remove_metadata(object):
    def setupUi(self, Dialog_remove_metadata):
        Dialog_remove_metadata.setObjectName("Dialog_remove_metadata")
        Dialog_remove_metadata.resize(384, 402)
        self.rmdd_dialogButtonBox = QtGui.QDialogButtonBox(Dialog_remove_metadata)
        self.rmdd_dialogButtonBox.setGeometry(QtCore.QRect(30, 360, 341, 32))
        self.rmdd_dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.rmdd_dialogButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.rmdd_dialogButtonBox.setObjectName("rmdd_dialogButtonBox")
        self.rmdd_frame = QtGui.QFrame(Dialog_remove_metadata)
        self.rmdd_frame.setGeometry(QtCore.QRect(20, 130, 351, 191))
        self.rmdd_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rmdd_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.rmdd_frame.setObjectName("rmdd_frame")
        self.gridLayoutWidget = QtGui.QWidget(self.rmdd_frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(90, 50, 251, 121))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.rmdd_gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.rmdd_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.rmdd_gridLayout.setObjectName("rmdd_gridLayout")
        self.chk_rem_exif_data = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chk_rem_exif_data.setObjectName("chk_rem_exif_data")
        self.rmdd_gridLayout.addWidget(self.chk_rem_exif_data, 0, 0, 1, 1)
        self.chk_rem_xmp_data = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chk_rem_xmp_data.setObjectName("chk_rem_xmp_data")
        self.rmdd_gridLayout.addWidget(self.chk_rem_xmp_data, 1, 0, 1, 1)
        self.chk_rem_iptc_data = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chk_rem_iptc_data.setObjectName("chk_rem_iptc_data")
        self.rmdd_gridLayout.addWidget(self.chk_rem_iptc_data, 3, 0, 1, 1)
        self.chk_rem_gps_data = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chk_rem_gps_data.setObjectName("chk_rem_gps_data")
        self.rmdd_gridLayout.addWidget(self.chk_rem_gps_data, 2, 0, 1, 1)
        self.chk_rem_all_metadata = QtGui.QCheckBox(self.rmdd_frame)
        self.chk_rem_all_metadata.setGeometry(QtCore.QRect(20, 20, 162, 17))
        self.chk_rem_all_metadata.setObjectName("chk_rem_all_metadata")
        self.rmdd_lbl = QtGui.QLabel(Dialog_remove_metadata)
        self.rmdd_lbl.setGeometry(QtCore.QRect(20, 10, 351, 111))
        self.rmdd_lbl.setWordWrap(True)
        self.rmdd_lbl.setObjectName("rmdd_lbl")

        self.retranslateUi(Dialog_remove_metadata)
        QtCore.QObject.connect(self.rmdd_dialogButtonBox, QtCore.SIGNAL("accepted()"), Dialog_remove_metadata.accept)
        QtCore.QObject.connect(self.rmdd_dialogButtonBox, QtCore.SIGNAL("rejected()"), Dialog_remove_metadata.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_remove_metadata)

    def retranslateUi(self, Dialog_remove_metadata):
        Dialog_remove_metadata.setWindowTitle(QtGui.QApplication.translate("Dialog_remove_metadata", "Remove metadata", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_rem_exif_data.setText(QtGui.QApplication.translate("Dialog_remove_metadata", "Remove exif data", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_rem_xmp_data.setText(QtGui.QApplication.translate("Dialog_remove_metadata", "Remove xmp data", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_rem_iptc_data.setText(QtGui.QApplication.translate("Dialog_remove_metadata", "Remove iptc data", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_rem_gps_data.setToolTip(QtGui.QApplication.translate("Dialog_remove_metadata", "gps data can be both in exif and xmp data", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_rem_gps_data.setText(QtGui.QApplication.translate("Dialog_remove_metadata", "Remove gps data", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_rem_all_metadata.setToolTip(QtGui.QApplication.translate("Dialog_remove_metadata", "(Un)Check this value will (un)check all underlying values", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_rem_all_metadata.setText(QtGui.QApplication.translate("Dialog_remove_metadata", "Remove all metadata", None, QtGui.QApplication.UnicodeUTF8))
        self.rmdd_lbl.setText(QtGui.QApplication.translate("Dialog_remove_metadata", "Which metadata do you want to remove from your selected image(s)?\n"
"Note that this screen is meant to move all tags from a certain category from your selected images(s).\n"
"By writing \"clean empty\" fields from the Edit tabs you can more specifically clean that metadata.", None, QtGui.QApplication.UnicodeUTF8))

