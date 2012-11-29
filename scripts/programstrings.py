# -*- coding: utf-8 -*-

# programstrings.py - This python "script" holds general texts for the other scripts

# Copyright (c) 2012 Harry van der Wolf. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.

# This file is part of pyexiftoolgui.
# pyexiftoolgui is a pySide script program that reads and writes  
# gps tags from/to files. It can use a "reference" image to write the
# gps tags to a multiple set of files that are taken at the same
# location.
# pyexiftoolgui is a graphical frontend for the open source
# command line tool exiftool by Phil Harvey, but it's not
# a complete exiftool gui: not at all.


# SUPPORTEDIMAGES is the list of exiftool supported images. If a new format is added to exiftool, simply add it to this (alphabetical) list
SUPPORTEDIMAGES     = ("*.3fr *.3g2 *.3gp2 *.3gp *.3gpp "
                       "*.acr *.afm *.acfm *.amfm *.ai *.ait *.aiff *.aif *.aifc *.ape *.arw *.asf *.avi "
                       "*.bmp *.dib *.btf "
                       "*.chm *.cos *.cr2 *.crw *.ciff *.cs1 "
                       "*.dcm *.dc3 *.dic *.dicm *.dcp *.dcr *.dfont *.divx *.djvu *.djv *.dng *.doc *.dot "
                       "*.docx *.docm *.dotx *.dotm *.dylib *.dv *.dvb "
                       "*.eip *.eps *.epsf *.ps *.erf *.exe *.dll *.exif *.exr "
                       "*.f4a *.f4b *.f4p *.f4v *.fff *.fla *.flac *.flv *.fpx "
                       "*.gif *.gz *.gzip *.hdp *.wdp *.hdr *.html *.htm *.xhtml "
                       "*.icc *.icm *.idml *.iiq *.ind *.indd *.indt *.inx *.itc "
                       "*.j2c *.jpc *.jp2 *.jpf *.j2k *.jpm *.jpx *.jpeg *.jpg "
                       "*.k25 *.kdc *.key *.kth *.la *.lnk "
                       "*.m2ts *.mts *.m2t *.ts *.m4a *.m4b *.m4p *.m4v *.mef *.mie *.miff *.mif *.mka *.mkv *.mks "
                       "*.mos *.mov *.qt *.mp3 *.mp4 *.mpc *.mpeg *.mpg *.m2v *.mpo *.mqv *.mrw *.mxf "
                       "*.nef *.nmbtemplate *.nrw *.numbers "
                       "*.odb *.odc *.odf *.odg *.odi *.odp *.ods *.odt *.ofr *.ogg *.ogv *.orf *.otf "
                       "*.pac *.pages *.pcd *.pdf *.pef *.pfa *.pfb *.pfm *.pgf *.pict *.pct *.pmp *.png *.jng *.mng "
                       "*.ppm *.pbm *.pgm *.ppt *.pps *.pot *.potx *.potm *.ppsx *.ppsm *.pptx *.pptm *.psd *.psb *.psp *.pspimage "
                       "*.qtif *.qti *.qif "
                       "*.ra *.raf *.ram *.rpm *.rar *.raw *.raw *.riff *.rif *.rm *.rv *.rmvb *.rsrc *.rtf *.rw2 *.rwl *.rwz "
                       "*.so *.sr2 *.srf *.srw *.svg *.swf "
                       "*.thm *.thmx *.tiff *.tif *.ttf *.ttc "
                       "*.vob *.vrd *.vsd *.wav *.webm *.webp *.wma *.wmv *.wv "
                       "*.x3f *.xcf *.xls *.xlt *.xlsx *.xlsm *.xlsb *.xltx *.xltm *.xmp")
MAPCOORDINATESHELP  = ("<p><b>Integrated MapCoordinates.net</b></p>"
                       "<p>MapCoordinates gives you an easy option to retrieve longitude, latitude and "
                       "altitude from your chosen and zoomed in location on the map. It uses Google Maps "
                       "to retrieve the information.</p>"
                       "<p>So how do you do that?</p>"
                       "<ul><li>Go to the Mapcoordinates.net tab.</li>"
                       "<li>Use the search bar to find your location.</li>"
                       "<li>This will display the latitude, longitude and altitude in a popup.</li>"
                       "<li>Copy this latitude, longitude and altitude data into the GPS tab input fields.</li></ul>"
                       "<p><b>Note:</b> The altitude is not always correct!! Check before copying!</p>"
                       "<p> It's not optimal but it helps.")

GPSHELP             = ("<p><b>Edit -> Gps tab information</b></p>"
                       "<p>This tab is used to add GPS data to your images. It will add "
                       "exif, xmp and iptc gps data to your images as some of the data in the different categories "
                       "is simply redundant (latitude, longitude) while other data is only partially "
                       "covered in a category, or uniquely in a category.</p>"
                       "<p>Buttons working on image(s):</p>"
                       "<ul><li><b>Copy from selected image</b>: This will copy all the (available) gps data from "
                       "the selected image into the input fields.</li>"
                       "<li><b>Save to selected image(s)</b>: This will save the gps data to your selected image(s).</li></ul>"
                       "General buttons:"
                       "<ul><li><b>Reset fields</b>: This will empty all fields and set radiobuttons and checkboxes to their defaults.</li>"
                       "<li><b>Help</b>: This button opens the popup you are currently looking at.</li></ul>"
                       "Calculator buttons:"
                       "<ul><li><b>Copy to input fields</b>: This copies the calculated values (bottom half) to the input fields (top half).</li>"
                       "<li><b>Decimal to Minutes-Seconds</b>: Convert decimal longitude/latitude values to deg-min-sec.</li>"
                       "<li><b>Minutes-Seconds to Decimal</b>: Convert deg-min-sec to decimal latitude/longitude (necessary for input).</li></ul>")

GPANOHELP             = ("<p><b>Edit -> GPano Google PhotoSphere tab information</b></p>"
                       "<p>This tab is used to add GPano Google PhotoSphere data to your selected image(s).</p>"
                       "<p>This functionality is only available if you have exiftool 9.07 or newer. You can always download "
                       "the latest <a href='http://www.sno.phy.queensu.ca/~phil/exiftool/'>exiftool</a> version. "
                       "On Windows and Mac OS X simply install it. On Linux you simply unpack the tar.gz to some "
                       " folder. After the install/unpack you can use the Preferences tab to select that version.</p>"
                       "<p><b>Things to take into account!</b></p>"
                       "As you can see the options all have a <b>Save</b> checkbox behind their input fields. "
                       "It means that this option will be saved when checked, even when the field is empty. "
                       "This also means that you can:"
                       "<ul><li>overwrite existing data with empty data \"by accident\".</li>"
                       "<li>deliberately overwrite existing data with data from empty fields.</li></ul>"
                       "<br>Available buttons:"
                       "<ul><li><b>Copy from selected image</b>: This will copy all the (available) gpano data from "
                       "the selected image into the input fields.</li>"
                       "<li><b>Save to selected image(s)</b>: This will save the \"checked\" gpano data to your selected image(s).</li>"
                       "<li><b>Reset fields</b>: This will empty all fields and set checkboxes to their defaults.</li>"
                       "<li><b>Help</b>: This button opens the popup you are currently looking at.</li></ul>")

EXIFHELP             = ("<p><b>Edit -> Exif tab information</b></p>"
                       "<p>This tab is used to add EXIF data to your selected image(s).</p>"
                       "<p><b>Things to take into account!</b></p>"
                       "As you can see the options all have a <b>Save</b> checkbox behind their input fields. "
                       "It means that this option will be saved when checked, even when the field is empty. "
                       "This also means that you can:"
                       "<ul><li>overwrite existing data with empty data \"by accident\".</li>"
                       "<li>deliberately overwrite existing data with data from empty fields.</li></ul>"
                       "<br>Available buttons:"
                       "<ul><li><b>Copy from selected image</b>: This will copy all the (available) exif data from "
                       "the selected image into the input fields.</li>"
                       "<li><b>Save to selected image(s)</b>: This will save the \"checked\" exif data to your selected image(s).</li>"
                       "<li><b>Reset fields</b>: This will empty all fields and set checkboxes to their defaults.</li>"
                       "<li><b>Help</b>: This button opens the popup you are currently looking at.</li></ul>")

# End of strings 

