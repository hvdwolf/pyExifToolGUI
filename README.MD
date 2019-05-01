# pyExifToolGUI

# !!! DISCONTINUED !!!
## I stopped the development of python pyside gui. My latest changes were somewhere in 2015. 
After that time a number of contributors added patches to further expand functionality or to fix bugs.
Contributors were (in alfabetical order): darkdragon-001, emteejay, GadgetSteve, jedi and jejimenez.
I really thank them for their contributions and hope I do not disappoint them too much.

**What's next?**
As I (involuntarily) started to program in java for Android some time ago (as nobody else did what I needed), I decided to convert my pyExifToolGUI to java. 
Java has some great advantages comparted to a Gui based python program:
* It is (also) cross platform
* It comes with the builtin Swing/AWT gui. No more tedious packaging (due to the pyside GUI) for every platform.
* The packaged apps are much smaller and a java jar runs on any platform that has a JRE (Java Runtime Environment), whether it is Linux, AIX, BSD, Windows, Mac OS/X, RiscOS, Sun Solaris, etc.

So I'm curently working on jExifToolGUI.

<hr>
The pyExifToolGUI website is https://hvdwolf.github.io/pyExifToolGUI/
<br><rr>
pyExifToolGui is a python pySide QT4 script program that reads and writes
exif, xmp and IPTC tags from/to image files using exiftool. It can use a
"reference" image as source image to copy data from. 
A strong point of this software is the ability to write the data,
copied or not from a source image, to multiple images at once.
The main goal for this tool was the ability to write gps data to my images as I
photograph a lot in buildings like Churches/Cathedrals and Musea (when allowed),
which means that the gps functionality of the camera doesn't function.
Next to the gps functionality pyExifToolGUI will slowly grow into a general 
exiftool Gui and will also write other tags to your images.
This pyExifToolGUI tool is also a geotagging tool as of version 0.4.

pyExifToolGui is a graphical frontend for the excellent open source
command line tool ExifTool(1) by Phil Harvey.
pyExifToolGui is not a complete ExifTool Gui, far from that.
I needed a tool to add gps data to my images and couldn't find one
and decided to write my own. 
"By accident" it contains more functions as ExifTool is a powerful tool
and once you have written the basic program Gui skeleton it is relatively easy
to add extra functionality, which is basically to add more exif/xmp/iptc 
tags and add them to the "write to image" function. This is a time consuming 
process but not a difficult one.

This program is completely free, but you can donate any amount to me to show
your appreciation. See the Help menu in the program or the link below (2).

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version
3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License for more details."
You should have received a copy of the GNU General Public
License along with this program.  If not, see www.gnu.org/licenses


(1): http://www.sno.phy.queensu.ca/~phil/exiftool/<br>
(2): http://members.home.nl/harryvanderwolf/pyexiftoolgui/donate.html


This file: Version 0.50, 2013-12-23, H van der Wolf
