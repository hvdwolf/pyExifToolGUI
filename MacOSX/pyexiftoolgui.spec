# -*- mode: python -*-
a = Analysis(['/Users/Shared/development/python_related/pyside/pyExifToolGUI-0.5.1/scripts/pyexiftoolgui.py'],
             pathex=['/Users/Shared/development/python_related/pyinstaller-2.0', '/Users/Shared/development/python_related/pyside/pyExifToolGUI-0.5.1/scripts/', '/Users/Shared/development/python_related/pyside/pyExifToolGUI-0.5.1/scripts/ui/'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.darwin/pyexiftoolgui', 'pyexiftoolgui'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='/Users/Shared/development/python_related/pyside/pyExifToolGUI-0.5.1/MacOSX/pyExifToolGUI.app/Contents/Resources/appIcon.icns' )
coll = COLLECT(exe,
               a.binaries +
               [('libpyside-python2.7.1.1.dylib', '/usr/lib/libpyside-python2.7.1.1.dylib', 'DATA')] +
               [('libshiboken-python2.7.1.1.dylib', '/usr/lib/libshiboken-python2.7.1.1.dylib', 'DATA')] +
               [('../Resources/qt.conf', '/Users/Shared/development/python_related/pyside/pyExifToolGUI-0.5.1/MacOSX/qt.conf', 'DATA')] +
               [('COPYING', '/Users/Shared/development/python_related/pyside/pyExifToolGUI-0.5.1/COPYING', 'DATA')] +
               [('../Resources/appIcon.icns', '/Users/Shared/development/python_related/pyside/pyExifToolGUI-0.5.1/MacOSX/appIcon.icns', 'DATA')] +
               [('../Info.plist', '/Users/Shared/development/python_related/pyside/pyExifToolGUI-0.5.1/MacOSX/Info.plist', 'DATA')] +
               [('../PkgInfo', '/Users/Shared/development/python_related/pyside/pyExifToolGUI-0.5.1/MacOSX/PkgInfo', 'DATA')] +
               [('../Resources/qt_menu.nib/classes.nib', '/Library/Frameworks/QtGui.framework/Versions/Current/Resources/qt_menu.nib/classes.nib', 'DATA')] +
               [('../Resources/qt_menu.nib/info.nib', '/Library/Frameworks/QtGui.framework/Versions/Current/Resources/qt_menu.nib/info.nib', 'DATA')] +
               [('../Resources/qt_menu.nib/keyedobjects.nib', '/Library/Frameworks/QtGui.framework/Versions/Current/Resources/qt_menu.nib/keyedobjects.nib', 'DATA')] +
               [('../plugins/imageformats/libqgif.dylib', '/Developer/Applications/Qt/plugins/imageformats/libqgif.dylib', 'DATA')] +
               [('../plugins/imageformats/libqico.dylib', '/Developer/Applications/Qt/plugins/imageformats/libqico.dylib', 'DATA')] +
               [('../plugins/imageformats/libqjpeg.dylib', '/Developer/Applications/Qt/plugins/imageformats/libqjpeg.dylib', 'DATA')] +
               [('../plugins/imageformats/libqmng.dylib', '/Developer/Applications/Qt/plugins/imageformats/libqmng.dylib', 'DATA')] +
               [('../plugins/imageformats/libqsvg.dylib', '/Developer/Applications/Qt/plugins/imageformats/libqsvg.dylib', 'DATA')] +
               [('../plugins/imageformats/libqtga.dylib', '/Developer/Applications/Qt/plugins/imageformats/libqtga.dylib', 'DATA')] +
               [('../plugins/imageformats/libqtiff.dylib', '/Developer/Applications/Qt/plugins/imageformats/libqtiff.dylib', 'DATA')], 
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'pyexiftoolgui'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'pyexiftoolgui.app'))
