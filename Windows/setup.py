import os, sys
from distutils.core import setup
import py2exe
from glob import glob

realfile = os.path.realpath(__file__)
realfile_dir = os.path.dirname(os.path.abspath(realfile))
#print "base_path " + base_path
#print "realfile " + realfile
#print "realfile_dir " + realfile_dir

if sys.path.count(realfile_dir) == 0:
        sys.path.insert(0, realfile_dir)
else:
        sys.path.append(realfile_dir)
# Add subfolders
sys.path.append( realfile_dir + "\\scripts" )
sys.path.append( realfile_dir + "\\ui")


#includes = ['..\\scripts\\petgfunctions', '..\\scripts\\programinfo', '..\\scripts\\programstrings',
#             '..\\scripts\\info_window', '..\\ui\ui_MainWindow' ]

#includes = ['\\Datadir\\python\\pyside\\pyExifToolGUI\\scripts\\petgfunctions.py',
#            '\\Datadir\\python\\pyside\\pyExifToolGUI\\scripts\\programinfo',
#            '\\Datadir\\python\\pyside\\pyExifToolGUI\\scripts\\programstrings',
#            '\\Datadir\\python\\pyside\\pyExifToolGUI\\scripts\\info_window',
#            '\\Datadir\\python\\pyside\\pyExifToolGUI\\ui\\ui_MainWindow' ]

#dll_includes = ['D:\\Python27\\DLLs\\MSVCP90.dll']

excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']

data_files = [("Microsoft.VC90.CRT", glob(r'.\Microsoft.VC90.CRT\*.*')),
              ("scripts", glob(r'..\scripts\*.pyc'))]

#setup(windows=['..\\pyexiftoolgui.py'], data_files=data_files)
setup(options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
#                          "includes": includes,
                          "excludes": excludes,
                          }
                },
      data_files=data_files,
      windows=['..\\scripts\\info_window.py'])

setup(options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
                          "excludes": excludes,
                          }
                },
      data_files=data_files,
      windows=['..\\pyexiftoolgui.py',
               '..\\scripts\\petgfunctions.py',
               '..\\scripts\\programinfo.py',
               '..\\scripts\\programstrings.py',
               '..\\scripts\\info_window.py',
               '..\\ui\\ui_MainWindow.py'])
