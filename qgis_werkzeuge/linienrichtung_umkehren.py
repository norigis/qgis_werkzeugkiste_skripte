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
# siehe auch:
# How can I switch line direction in QGIS?
# https://gis.stackexchange.com/questions/9261/how-can-i-switch-line-direction-in-qgis
#------------------------------------------------------------

# Eingabedialog erstellen
##nori QGIS Werkzeuge=group
##Linienrichtung umkehren=name
##Eingabelayer=vector
##Nur_gewaehlte_Objekte=boolean true

from PyQt5.QtCore import *
from qgis.core import *

# Eingabedialog Parameter uebernehmen
eingabelayer = processing.getObject(Eingabelayer)
gewaehlte_objekte = Nur_gewaehlte_Objekte

# Eingabegeometrie pruefen
if eingabelayer.geometryType() != 1:
    raise RuntimeError('Eingabelayer wird nicht unterstuetzt. Nur Liniengeometrien sind zulaessig.')

# Checkbox "Nur gewaehlte Objekte" pruefen
if gewaehlte_objekte is True and eingabelayer.selectedFeatureCount() == 0:
    raise RuntimeError('Keine Objekte fuer Layer \'' + eingabelayer.name() + '\' gewaehlt.')

# Bearbeitungsstatus ueberpruefen
if not eingabelayer.isEditable():
    eingabelayer.startEditing()

# Linienrichtung umkehren
def reverse():
    geom = feature.geometry()
    nodes = geom.asPolyline()
    nodes.reverse()
    newgeom = QgsGeometry.fromPolyline(nodes)
    eingabelayer.changeGeometry(feature.id(),newgeom)

if gewaehlte_objekte is True:
    for feature in eingabelayer.selectedFeatures():
        reverse()
else:
    for feature in eingabelayer.getFeatures():
        reverse()

# Eingabelayer aktualisieren
eingabelayer.dataProvider().forceReload()
