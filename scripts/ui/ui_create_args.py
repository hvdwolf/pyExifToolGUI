# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_args.ui'
#
# Created: Sat Dec  7 12:11:39 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog_create_args(object):
    def setupUi(self, Dialog_create_args):
        Dialog_create_args.setObjectName("Dialog_create_args")
        Dialog_create_args.resize(392, 338)
        self.qdca_dialogButtonBox = QtGui.QDialogButtonBox(Dialog_create_args)
        self.qdca_dialogButtonBox.setGeometry(QtCore.QRect(30, 290, 341, 32))
        self.qdca_dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.qdca_dialogButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.qdca_dialogButtonBox.setObjectName("qdca_dialogButtonBox")
        self.rmdd_frame = QtGui.QFrame(Dialog_create_args)
        self.rmdd_frame.setGeometry(QtCore.QRect(20, 60, 351, 211))
        self.rmdd_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rmdd_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.rmdd_frame.setObjectName("rmdd_frame")
        self.gridLayoutWidget = QtGui.QWidget(self.rmdd_frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(70, 50, 271, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.rmdd_gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.rmdd_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.rmdd_gridLayout.setObjectName("rmdd_gridLayout")
        self.qdca_chk_args_exif_data = QtGui.QCheckBox(self.gridLayoutWidget)
        self.qdca_chk_args_exif_data.setObjectName("qdca_chk_args_exif_data")
        self.rmdd_gridLayout.addWidget(self.qdca_chk_args_exif_data, 0, 0, 1, 1)
        self.qdca_chk_args_xmp_data = QtGui.QCheckBox(self.gridLayoutWidget)
        self.qdca_chk_args_xmp_data.setObjectName("qdca_chk_args_xmp_data")
        self.rmdd_gridLayout.addWidget(self.qdca_chk_args_xmp_data, 1, 0, 1, 1)
        self.qdca_chk_args_iptc_data = QtGui.QCheckBox(self.gridLayoutWidget)
        self.qdca_chk_args_iptc_data.setObjectName("qdca_chk_args_iptc_data")
        self.rmdd_gridLayout.addWidget(self.qdca_chk_args_iptc_data, 3, 0, 1, 1)
        self.qdca_chk_args_gps_data = QtGui.QCheckBox(self.gridLayoutWidget)
        self.qdca_chk_args_gps_data.setObjectName("qdca_chk_args_gps_data")
        self.rmdd_gridLayout.addWidget(self.qdca_chk_args_gps_data, 2, 0, 1, 1)
        self.qdca_chk_args_iccprofile_data = QtGui.QCheckBox(self.gridLayoutWidget)
        self.qdca_chk_args_iccprofile_data.setObjectName("qdca_chk_args_iccprofile_data")
        self.rmdd_gridLayout.addWidget(self.qdca_chk_args_iccprofile_data, 4, 0, 1, 1)
        self.qdca_chk_args_all_metadata = QtGui.QCheckBox(self.rmdd_frame)
        self.qdca_chk_args_all_metadata.setGeometry(QtCore.QRect(20, 20, 201, 17))
        self.qdca_chk_args_all_metadata.setObjectName("qdca_chk_args_all_metadata")
        self.qdca_lbl = QtGui.QLabel(Dialog_create_args)
        self.qdca_lbl.setGeometry(QtCore.QRect(20, 10, 351, 41))
        self.qdca_lbl.setWordWrap(True)
        self.qdca_lbl.setObjectName("qdca_lbl")

        self.retranslateUi(Dialog_create_args)
        QtCore.QObject.connect(self.qdca_dialogButtonBox, QtCore.SIGNAL("accepted()"), Dialog_create_args.accept)
        QtCore.QObject.connect(self.qdca_dialogButtonBox, QtCore.SIGNAL("rejected()"), Dialog_create_args.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_create_args)
        Dialog_create_args.setTabOrder(self.qdca_chk_args_all_metadata, self.qdca_chk_args_exif_data)
        Dialog_create_args.setTabOrder(self.qdca_chk_args_exif_data, self.qdca_chk_args_xmp_data)
        Dialog_create_args.setTabOrder(self.qdca_chk_args_xmp_data, self.qdca_chk_args_gps_data)
        Dialog_create_args.setTabOrder(self.qdca_chk_args_gps_data, self.qdca_chk_args_iptc_data)
        Dialog_create_args.setTabOrder(self.qdca_chk_args_iptc_data, self.qdca_chk_args_iccprofile_data)
        Dialog_create_args.setTabOrder(self.qdca_chk_args_iccprofile_data, self.qdca_dialogButtonBox)

    def retranslateUi(self, Dialog_create_args):
        Dialog_create_args.setWindowTitle(QtGui.QApplication.translate("Dialog_create_args", "Create args file(s) from selected image(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.qdca_chk_args_exif_data.setText(QtGui.QApplication.translate("Dialog_create_args", "Add exif data to args file(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.qdca_chk_args_xmp_data.setText(QtGui.QApplication.translate("Dialog_create_args", "Add xmp data to args file(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.qdca_chk_args_iptc_data.setText(QtGui.QApplication.translate("Dialog_create_args", "Add iptc data to args file(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.qdca_chk_args_gps_data.setToolTip(QtGui.QApplication.translate("Dialog_create_args", "gps data can be both in exif and xmp data", None, QtGui.QApplication.UnicodeUTF8))
        self.qdca_chk_args_gps_data.setText(QtGui.QApplication.translate("Dialog_create_args", "Add gps data to args file(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.qdca_chk_args_iccprofile_data.setText(QtGui.QApplication.translate("Dialog_create_args", "Add ICC profile data to args file(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.qdca_chk_args_all_metadata.setToolTip(QtGui.QApplication.translate("Dialog_create_args", "(Un)Check this value will (un)check all underlying values", None, QtGui.QApplication.UnicodeUTF8))
        self.qdca_chk_args_all_metadata.setText(QtGui.QApplication.translate("Dialog_create_args", "Add all metadata to args file(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.qdca_lbl.setText(QtGui.QApplication.translate("Dialog_create_args", "Which metadata from your selected image(s) do you want to add to your args file(s)?\n"
"", None, QtGui.QApplication.UnicodeUTF8))

