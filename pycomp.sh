#!/bin/sh
# Small shell script to do some of the dirty work for me.
# 20121212, V 1.0, HvdW. 

cd scripts/ui
pyside-uic create_args.ui > ui_create_args.py
pyside-uic export_metadata.ui > ui_export_metadata.py
pyside-uic modifydatetime.ui > ui_modifydatetime.py
pyside-uic remove_metadata.ui > ui_remove_metadata.py
pyside-uic MainWindow.ui > ui_MainWindow.py
#pyside-uic MainWindow.ui > ui_MainWindowMAC.py
sed -e "s+MainWindow.setMenuBar(self+#MainWindow.setMenuBar(self+" ui_MainWindow.py > ui_MainWindowMAC.py
