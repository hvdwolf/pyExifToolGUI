# -*- mode: python -*-
a = Analysis(['..\\pyside\\pyexiftoolgui-git\\scripts\\pyexiftoolgui.py'],
             pathex=['D:\\LocalData_387640\\Datadir\\python\\pyinstaller-2.0', '..\\pyside\\pyexiftoolgui-git\\scripts\\', '..\\pyside\\pyexiftoolgui-git\\scripts\\ui'],
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
          console=False , icon='..\\pyside\\pyexiftoolgui-git\\logo\\pyexiftoolgui.ico')
coll = COLLECT(exe,
               a.binaries +
               [('qt.conf', '..\\pyside\\pyexiftoolgui-git\\Windows\\qt.conf', 'DATA')] +
               [('plugins\\imageformats\\qjpeg4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qjpeg4.dll', 'DATA')] +
               [('plugins\\imageformats\\qgif4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qgif4.dll', 'DATA')] +
               [('plugins\\imageformats\\qmng4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qmng4.dll', 'DATA')] +
               [('plugins\\imageformats\\qsvgg4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qsvg4.dll', 'DATA')] +
               [('plugins\\imageformats\\qtiff4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qtiff4.dll', 'DATA')] +
               [('plugins\\imageformats\\qico4.dll', 'D:\\LocalData_387640\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qico4.dll', 'DATA')] +
               [('COPYING', '..\\pyside\\pyexiftoolgui-git\\COPYING', 'DATA')] ,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'pyexiftoolgui'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'pyexiftoolgui.app'))
