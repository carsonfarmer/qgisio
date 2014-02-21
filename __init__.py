# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgisio
                                 A QGIS plugin
 A tool to shoot vector layers from QGIS to geojson.oi
                             -------------------
        begin                : 2014-02-19
        copyright            : (C) 2014 by Carson J. Q. Farmer
        email                : carson.farmer@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load QgisIO class from file QgisIO
    from qgisio import QgisIO
    return QgisIO(iface)
