# -*- mode: python -*-
a = Analysis(['..\\pyside\\pyexiftoolgui-hg\\scripts\\pyexiftoolgui.py'],
             pathex=['D:\\Datadir\\python\\pyinstaller-2.0'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\pyexiftoolgui', 'pyexiftoolgui.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='..\\pyside\\pyexiftoolgui-hg\\logo\\pyexiftoolgui.ico')
coll = COLLECT(exe,
               a.binaries +
               [('petgfunctions.py', '..\\pyside\\pyexiftoolgui-hg\\scripts\\petgfunctions.py', 'PYSOURCE')] +
               [('programstrings.py', '..\\pyside\\pyexiftoolgui-hg\\scripts\\programstrings.py', 'PYSOURCE')] +
               [('programinfo.py', '..\\pyside\\pyexiftoolgui-hg\\scripts\\programinfo.py', 'PYSOURCE')] +
               [('ui_MainWindow.py', '..\\pyside\\pyexiftoolgui-hg\\scripts\\ui\\ui_MainWindow.py', 'PYSOURCE')] +
               [('qt.conf', '..\\pyside\\pyexiftoolgui-hg\\Windows\\qt.conf', 'DATA')] +
               [('plugins\\imageformats\\qjpeg4.dll', 'D:\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qjpeg4.dll', 'DATA')] +
               [('plugins\\imageformats\\qgif4.dll', 'D:\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qgif4.dll', 'DATA')] +
               [('plugins\\imageformats\\qmng4.dll', 'D:\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qmng4.dll', 'DATA')] +
               [('plugins\\imageformats\\qsvgg4.dll', 'D:\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qsvg4.dll', 'DATA')] +
               [('plugins\\imageformats\\qtiff4.dll', 'D:\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qtiff4.dll', 'DATA')] +
               [('plugins\\imageformats\\qico4.dll', 'D:\\python27\\Lib\\site-packages\\PySide\\plugins\\imageformats\\qico4.dll', 'DATA')] +
               [('COPYING.txt', '..\\pyside\\pyexiftoolgui-hg\\COPYING', 'DATA')] ,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'pyexiftoolgui'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'pyexiftoolgui.app'))
