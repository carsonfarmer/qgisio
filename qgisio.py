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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
#from qgisiodialog import QgisIODialog
# System imports
import os.path, os, sys
from tempfile import mkstemp
import webbrowser
# Local imports
from .geojsonio import _create_gist

class QgisIO:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n',
            'qgisio_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Don't really need a dialog...
        ## Create the dialog (after translation) and keep reference
        #self.dlg = QgisIODialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/qgisio/icon.png"),
            u"Shoot layer", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&qgisio", self.action)
        
        # Create a help action that will provide some extra info
        self.help = QAction(
            QIcon(":/plugins/qgisio/help.png"),
            u"&Help", self.iface.mainWindow())
        self.help.triggered.connect(self.show_help)
        self.iface.addPluginToMenu(u"&qgisio", self.help)
        
    def show_help(self):
        help_file = "file://" + os.path.join(self.plugin_dir, 
            "help/index.html")
        # For testing path:
        #QMessageBox.information(None, "Help File", help_file)
        res = QDesktopServices.openUrl(QUrl(help_file))

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&qgisio", self.action)
        self.iface.removePluginMenu(u"&qgisio", self.help)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        # Some code to save current layer as GeoJSON

        layer = self.iface.activeLayer()
        try:
            name = layer.name()
        except AttributeError:
            QMessageBox.critical(self.iface.mainWindow(), "Error", 
                "No layer selected!")
            return
        
        if not layer.type() == QgsMapLayer.VectorLayer:
            QMessageBox.critical(self.iface.mainWindow(), "Error", 
                "Can only shoot vector layers!")
            return
            
        has_selection = bool(layer.selectedFeatureCount())
        ltype = layer.storageType()

        # Create a temp file to export to GeoJSON with
        handle, tempfile = mkstemp(suffix='.geojson')
        os.close(handle) # Close it right away (but it won't be deleted)

        # Export current layer to GeoJSON
        crs = QgsCoordinateReferenceSystem(4326, # GeoJSON should be in 4326...
            QgsCoordinateReferenceSystem.PostgisCrsId)
        error = QgsVectorFileWriter.writeAsVectorFormat(layer, tempfile,
            "utf-8", crs, "GeoJSON", onlySelected=has_selection)
        if error != QgsVectorFileWriter.NoError:
            message = "Unable to write layer to GeoJSON file for display at geojson.io"
            self.iface.messageBar().pushMessage("Write error", message, 
                level=QgsMessageBar.CRITICAL, duration=3)
            return

        # Ok, let's grab the contents and shoot it to geojson.io
        with open(str(tempfile), 'r') as f:
            contents = f.read()
        os.remove(tempfile)

        url = _create_gist(contents, "Layer exported from QGIS", 
            name + ".geojson")
        
        # Let the user know it all worked nicely
        def open_browser():
            QDesktopServices.openUrl(QUrl(url))

        widget = self.iface.messageBar().createMessage("Layer shot to", url)
        button = QPushButton(widget)
        button.setText("Show me!") # Give option to open browser
        button.pressed.connect(open_browser)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, QgsMessageBar.INFO)
        QgsMessageLog.logMessage("qgisio - Layer shot to: %s" % url)
        gist_domain = "https://gist.github.com"
        gist_id = url[url.rfind('/')+1:]
        QgsMessageLog.logMessage("qgisio - Raw Gist link: %s/%s" % (gist_domain, 
            gist_id))

def add_unique_postfix(fn):
    '''
    Function for making unique non-existent file name 
    with saving source file extension
    
    Author:
    Denis Barmenkov <denis.barmenkov@gmail.com>
    Code Source:
    http://code.activestate.com/recipes/577200-make-unique-file-name/
    '''

    if not os.path.exists(fn):
        return fn

    path, name = os.path.split(fn)
    name, ext = os.path.splitext(name)

    make_fn = lambda i: os.path.join(path, '%s(%d)%s' % (name, i, ext))

    for i in xrange(2, sys.maxint):
        uni_fn = make_fn(i)
        if not os.path.exists(uni_fn):
            return uni_fn

    return None
