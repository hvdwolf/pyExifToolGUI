# -*- mode: python -*-
a = Analysis(['../pyside/pyexiftoolgui-hg/scripts/pyexiftoolgui.py'],
             pathex=['/Users/Shared/development/python_related/pyinstaller-2.0', '../pyside/pyexiftoolgui-hg/scripts/', '../pyside/pyexiftoolgui-hg/scripts/ui/'],
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
          console=False , icon='../pyside/pyexiftoolgui-hg/MacOSX/pyExifToolGUI.app/Contents/Resources/appIcon.icns' )
coll = COLLECT(exe,
               a.binaries +
               [('qt.conf', '../pyside/pyexiftoolgui-hg/Windows/qt.conf', 'DATA')] +
               [('COPYING', '../pyside/pyexiftoolgui-hg/COPYING', 'DATA')] ,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'pyexiftoolgui'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'pyexiftoolgui.app'))
