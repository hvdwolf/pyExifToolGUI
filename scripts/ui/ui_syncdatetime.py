# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'syncdatetime.ui'
#
# Created: Sat Dec  7 12:11:39 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SyncDateTimeTagsDialog(object):
    def setupUi(self, SyncDateTimeTagsDialog):
        SyncDateTimeTagsDialog.setObjectName("SyncDateTimeTagsDialog")
        SyncDateTimeTagsDialog.resize(437, 240)
        self.buttonBox = QtGui.QDialogButtonBox(SyncDateTimeTagsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtGui.QWidget(SyncDateTimeTagsDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 60, 391, 111))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.qdsdtt_modifydate = QtGui.QLineEdit(self.gridLayoutWidget)
        self.qdsdtt_modifydate.setMaximumSize(QtCore.QSize(180, 16777215))
        self.qdsdtt_modifydate.setObjectName("qdsdtt_modifydate")
        self.gridLayout.addWidget(self.qdsdtt_modifydate, 2, 1, 1, 1)
        self.qdsdtt_datetimeoriginal = QtGui.QLineEdit(self.gridLayoutWidget)
        self.qdsdtt_datetimeoriginal.setMaximumSize(QtCore.QSize(180, 16777215))
        self.qdsdtt_datetimeoriginal.setObjectName("qdsdtt_datetimeoriginal")
        self.gridLayout.addWidget(self.qdsdtt_datetimeoriginal, 0, 1, 1, 1)
        self.qdsdtt_modifydate_2 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.qdsdtt_modifydate_2.setMaximumSize(QtCore.QSize(180, 16777215))
        self.qdsdtt_modifydate_2.setObjectName("qdsdtt_modifydate_2")
        self.gridLayout.addWidget(self.qdsdtt_modifydate_2, 1, 1, 1, 1)
        self.radioButton_qdsdtt_dto = QtGui.QRadioButton(self.gridLayoutWidget)
        self.radioButton_qdsdtt_dto.setChecked(True)
        self.radioButton_qdsdtt_dto.setObjectName("radioButton_qdsdtt_dto")
        self.gridLayout.addWidget(self.radioButton_qdsdtt_dto, 0, 2, 1, 1)
        self.radioButton_qdsdtt_cd = QtGui.QRadioButton(self.gridLayoutWidget)
        self.radioButton_qdsdtt_cd.setObjectName("radioButton_qdsdtt_cd")
        self.gridLayout.addWidget(self.radioButton_qdsdtt_cd, 1, 2, 1, 1)
        self.radioButton_qdsdtt_md = QtGui.QRadioButton(self.gridLayoutWidget)
        self.radioButton_qdsdtt_md.setObjectName("radioButton_qdsdtt_md")
        self.gridLayout.addWidget(self.radioButton_qdsdtt_md, 2, 2, 1, 1)
        self.chk_qdsdtt_use_referencedata = QtGui.QCheckBox(SyncDateTimeTagsDialog)
        self.chk_qdsdtt_use_referencedata.setGeometry(QtCore.QRect(30, 30, 391, 21))
        self.chk_qdsdtt_use_referencedata.setObjectName("chk_qdsdtt_use_referencedata")
        self.chk_qdsdtt_updatexmp = QtGui.QCheckBox(SyncDateTimeTagsDialog)
        self.chk_qdsdtt_updatexmp.setGeometry(QtCore.QRect(30, 180, 351, 17))
        self.chk_qdsdtt_updatexmp.setObjectName("chk_qdsdtt_updatexmp")

        self.retranslateUi(SyncDateTimeTagsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SyncDateTimeTagsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SyncDateTimeTagsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SyncDateTimeTagsDialog)

    def retranslateUi(self, SyncDateTimeTagsDialog):
        SyncDateTimeTagsDialog.setWindowTitle(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "Synchronize DateTime tags", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "DateTimeOriginal", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "ModifyDate", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "CreateDate", None, QtGui.QApplication.UnicodeUTF8))
        self.qdsdtt_modifydate.setInputMask(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "9999:99:99 99:99:99; ", None, QtGui.QApplication.UnicodeUTF8))
        self.qdsdtt_datetimeoriginal.setInputMask(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "9999:99:99 99:99:99; ", None, QtGui.QApplication.UnicodeUTF8))
        self.qdsdtt_modifydate_2.setInputMask(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "9999:99:99 99:99:99; ", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_qdsdtt_dto.setText(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "Use as source", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_qdsdtt_cd.setText(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "Copy here", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_qdsdtt_md.setText(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "Copy here", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_qdsdtt_use_referencedata.setText(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "Use date and time from reference image", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_qdsdtt_updatexmp.setText(QtGui.QApplication.translate("SyncDateTimeTagsDialog", "Update xmp values as well", None, QtGui.QApplication.UnicodeUTF8))

