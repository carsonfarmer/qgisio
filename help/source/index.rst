.. qgisio documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to qgisio's documentation!
==================================

.. index:: About

About
=====

**qgisio** is a quick and simple way to shoot any **QGIS** vector layer to **geojson.io** for quick viewing, editing, and sharing with others. If you are working with a relatively large vector layer, it will automatically upload the generated GeoJSON to an anonymous `GitHub <https://github.com/>`_ `Gist <https://gist.github.com>`_ for viewing at `geojson.io <http://geojson.io/>`_. From there, you can save it to one of your own GitHub repos, delete it, or do whatever you like -- its your data!

.. index:: What; More

What *is* geojson.io?
---------------------

geojson.io is a quick, simple tool for creating, viewing, and sharing maps. geojson.io is named after `GeoJSON <http://geojson.org/>`_, an open source data format, and it supports GeoJSON in all ways -- but also accepts KML, GPX, CSV, TopoJSON, and other formats. Checkout the `geojson.io ?Help <http://geojson.io/>`_ for more details. Central to geojson.io is GitHub and Gists. A Gist is a simple way to share snippets and pastes with others (including snippets of data!). All gists are Git repositories, so they are automatically versioned, forkable and usable from Git. If you don't know what Git is, then `head here <http://git-scm.com/>`_ and find out!

.. index:: licensing
.. index:: License; Privacy; Issues

Privacy & License Issues
========================

The code to shoot your layers to geojson.io is released under various open source licenses (see COPYRIGHT file in source directory), but that doesn't mean your data has to be public or open source. Once you've shot your data to geojson.io, clicking save by default saves to a private GitHub Gist -- so it will only be accessible to people you share the URL with, and creating it won't appear in your GitHub timeline.
The data you create and modify in geojson.io doesn't acquire any additional license: if it's secret and copyrighted, it will remain that way.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`