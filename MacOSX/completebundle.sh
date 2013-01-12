#!/bin/sh
# To be run from MacOSX folder

curpath=`pwd`
App="$curpath/dist/pyexiftoolgui.app"
imgdylibfolder="$App/Contents/plugins/imageformats"
MacOSfolder="$App/Contents/MacOS"

# First do the image dylibs in plugins/imageformats
cd "$imgdylibfolder"
for i in *.dylib; do install_name_tool -change QtGui.framework/Versions/4/QtGui @executable_path/QtGui $i; done
for i in *.dylib; do install_name_tool -change QtCore.framework/Versions/4/QtCore @executable_path/QtCore $i; done
for i in *.dylib; do install_name_tool -id @executable_path/../plugins/imageformats/$i $i; done


# Now do everything in the MacOS folder
cd "$MacOSfolder"

# Some things are double but better too much actions then too little
for i in *.dylib; do install_name_tool -change QtGui.framework/Versions/4/QtGui @executable_path/QtGui $i; done
for i in *.dylib; do install_name_tool -change QtCore.framework/Versions/4/QtCore @executable_path/QtCore $i; done
for i in *.dylib; do install_name_tool -change  libshiboken-python2.7.1.1.dylib @executable_path/libshiboken-python2.7.1.1.dylib $i; done
for i in *.dylib; do install_name_tool -change  libpyside-python2.7.1.1.dylib @executable_path/libpyside-python2.7.1.1.dylib $i; done
for i in *.dylib; do install_name_tool -id @executable_path/$i $i; done


binaries="*.so *.dylib Qt* Python" 

for exec_file in $binaries
do

 echo "Processing: $exec_file"

 echo "First do the own $old_install_name_dirname"
  for lib in $(otool -D $exec_file | grep @loader_path | sed -e 's/ (.*$//' -e 's/^.*\///')
  do
   echo " Changing own install name."
   install_name_tool -id "@executable_path/$lib" $exec_file
  done

 for lib in $(otool -L $exec_file | grep @loader_path | sed -e 's/ (.*$//' -e 's/^.*\///')
 do
  echo " Changing install name for: $lib"
  install_name_tool -change "@loader_path/$lib" "@executable_path/$lib" $exec_file
 done
done

# Copy the Gnu license file into the bundle
cp -a "$curpath/../COPYING" "$App/Contents/Resources"  

# Finally copy the manual into the bundle
cp -a "$curpath/../manual" "$MacOSfolder"

