#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------
# (c) 2017 by noriGIS
# norigis@posteo.at
#------------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#------------------------------------------------------------

# Eingabedialog erstellen
##nori QGIS Werkzeuge=group
##Blattschnittgenerator=name
##Eingabelayer=vector
##Massstab=string 1:1000
##Format=selection A0;A1;A2;A3;A4;A5
##Orientierung=selection Querformat;Hochformat
##Raender_x_in_mm=number 5
##Raender_y_in_mm=number 5
##Ursprung_x=number 0
##Ursprung_y=number 0

from PyQt5.QtCore import *
from qgis.core import *
from decimal import Decimal

# Eingabedialog Parameter uebernehmen
eingabelayer = processing.getObject(Eingabelayer)
massstab = Massstab
format = Format
orientierung = Orientierung
rand_x = Raender_x_in_mm
rand_y = Raender_y_in_mm
ursprung_x = Ursprung_x
ursprung_y = Ursprung_y

# Massstab in 'Float' umwandeln
massstab = massstab[2:]
massstab = float(massstab)

# Eingabegeometrie pruefen
if eingabelayer.geometryType() != 2:
    raise RuntimeError('Eingabelayer wird nicht unterstuetzt. Nur Polygongeometrien sind zulaessig.')

# Bearbeitungsstatus ueberpruefen
if not eingabelayer.isEditable():
    eingabelayer.startEditing()

# Formate ermitteln 
if format == 0 and orientierung == 0:
    format_breite = 1.189
    format_hoehe = 0.841
    format = 'A0'
elif format == 0 and orientierung == 1:
    format_breite = 0.841
    format_hoehe = 1.189
    format = 'A0'
elif format == 1 and orientierung == 0:
    format_breite = 0.841
    format_hoehe = 0.594
    format = 'A1'
elif format == 1 and orientierung == 1:
    format_breite = 0.594
    format_hoehe = 0.841
    format = 'A1'
elif format == 2 and orientierung == 0:
    format_breite = 0.594
    format_hoehe = 0.42
    format = 'A2'
elif format == 2 and orientierung == 1:
    format_breite = 0.42
    format_hoehe = 0.594
    format = 'A2'
elif format == 3 and orientierung == 0:
    format_breite = 0.42
    format_hoehe = 0.297
    format = 'A3'
elif format == 3 and orientierung == 1:
    format_breite = 0.297
    format_hoehe = 0.42
    format = 'A3'
elif format == 4 and orientierung == 0:
    format_breite = 0.297
    format_hoehe = 0.21
    format = 'A4'
elif format == 4 and orientierung == 1:
    format_breite = 0.21
    format_hoehe = 0.297
    format = 'A4'
elif format == 5 and orientierung == 0:
    format_breite = 0.21
    format_hoehe = 0.148
    format = 'A5'
elif format == 5 and orientierung == 1:
    format_breite = 0.148
    format_hoehe = 0.21
    format = 'A5'

# Rand beruecksichtigen
rand_x = rand_x / 1000
rand_y = rand_y / 1000
rand_x = rand_x * 2
rand_y = rand_y * 2

karte_breite = format_breite - rand_x
karte_hoehe = format_hoehe - rand_y

# Blattschnittpolygon ermitteln
blattschnitt_breite = karte_breite * massstab
blattschnitt_hoehe = karte_hoehe * massstab

# Koordinaten ermitteln
x1 = ursprung_x
y1 = ursprung_y

x2 = x1
y2 = y1 + blattschnitt_hoehe

x3 = x1 + blattschnitt_breite
y3 = y1 + blattschnitt_hoehe

x4 = x1 + blattschnitt_breite
y4 = y1

# Polygon erstellen
seg = QgsFeature() 
seg.setGeometry(QgsGeometry.fromPolygon([[QgsPoint(x1, y1), QgsPoint(x2, y2), QgsPoint(x3, y3), QgsPoint(x4, y4)]]))
eingabelayer.addFeatures([seg])

# Protokollinformation erstellen
format_breite = format_breite * 1000
format_hoehe = format_hoehe * 1000

karte_breite = karte_breite * 1000
karte_hoehe = karte_hoehe * 1000

rand_x = rand_x / 2
rand_y = rand_y / 2
rand_x = rand_x * 1000
rand_y = rand_y * 1000

def format_float(f):
    d = Decimal(str(f));
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
    # (siehe https://stackoverflow.com/a/36981428)

massstab = format_float(massstab)
blattschnitt_breite = format_float(blattschnitt_breite)
blattschnitt_hoehe = format_float(blattschnitt_hoehe)
format_breite = format_float(format_breite)
format_hoehe = format_float(format_hoehe)
karte_breite = format_float(karte_breite)
karte_hoehe = format_float(karte_hoehe)
rand_x = format_float(rand_x)
rand_y = format_float(rand_y)

progress.setInfo('')
progress.setInfo('***** Blattschnittinformation *****')
progress.setInfo('')
progress.setInfo('Massstab: 1:' + str(massstab))
progress.setInfo('')
progress.setInfo('Breite Blattschnittpolygon: ' + str(blattschnitt_breite) + ' m')
progress.setInfo('Hoehe Blattschnittpolygon: ' + str(blattschnitt_hoehe) + ' m')
progress.setInfo('')
progress.setInfo('Format: ' + str(format) + ' (' + str(format_breite) + ' x ' + str(format_hoehe) + ' mm)')
progress.setInfo('')
progress.setInfo('Breite Karte in Druckzusammenstellung: ' + str(karte_breite) + ' mm')
progress.setInfo('Hoehe Karte in Druckzusammenstellung: ' + str(karte_hoehe) + ' mm')
progress.setInfo('')
progress.setInfo('Raender x: ' + str(rand_x) + ' mm')
progress.setInfo('Raender y: ' + str(rand_y) + ' mm')
progress.setInfo('')
progress.setInfo('***********************************')
progress.setInfo('')
