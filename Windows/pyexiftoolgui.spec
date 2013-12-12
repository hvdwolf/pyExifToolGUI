# -*- mode: python -*-
a = Analysis(['..\\pyside\\pyexiftoolgui-0.4.0.1\\scripts\\pyexiftoolgui.py'],
             pathex=['D:\\LocalData_387640\\Datadir\\python\\pyinstaller-2.0', '..\\pyside\\pyexiftoolgui-0.4.0.1\\scripts\\', '..\\pyside\\pyexiftoolgui-0.4.0.1\\scripts\\ui'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure )
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\pyexiftoolgui', 'pyexiftoolgui.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='..\\pyside\\pyexiftoolgui-0.4.0.1\\logo\\pyexiftoolgui.ico')
coll = COLLECT(exe,
               a.binaries +
               [('qt.conf', '..\\pyside\\pyexiftoolgui-0.4.0.1\\Windows\\qt.conf', 'DATA')] +
               [('plugins\\imageformats\\qjpeg4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qjpeg4.dll', 'DATA')] +
               [('plugins\\imageformats\\qgif4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qgif4.dll', 'DATA')] +
               [('plugins\\imageformats\\qmng4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qmng4.dll', 'DATA')] +
               [('plugins\\imageformats\\qsvgg4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qsvg4.dll', 'DATA')] +
               [('plugins\\imageformats\\qtiff4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qtiff4.dll', 'DATA')] +
               [('plugins\\imageformats\\qico4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qico4.dll', 'DATA')] +
               [('COPYING', '..\\pyside\\pyexiftoolgui-0.4.0.1\\COPYING', 'DATA')] +
               [('README.txt', '..\\pyside\\pyexiftoolgui-0.4.0.1\\README.txt', 'DATA')] +
               [('Changelog', '..\\pyside\\pyexiftoolgui-0.4.0.1\\Changelog', 'DATA')] ,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'pyexiftoolgui'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'pyexiftoolgui.app'))
