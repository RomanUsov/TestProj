#!/usr/bin/env python
#
# MapBox tile generator written by 
# Tom MacWright <macwright [-at-] gmail.com>, based on 
# gdal2tiles.py, whose license and author are noted below
#
###############################################################################
# Project:  Google Summer of Code 2007
# Purpose:  Convert a raster into TMS tiles, create KML SuperOverlay EPSG:4326,
#           generate a simple HTML viewers based on Google Maps and OpenLayers
# Author:   Klokan Petr Pridal, klokan at klokan dot cz
# Web:      http://www.klokan.cz/projects/gdal2tiles/
###############################################################################
# Copyright (c) 2007, Klokan Petr Pridal
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
###############################################################################

# image legend
# <img src="data:image/png;base64, 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" alt= "S2A.png" />

from osgeo import gdal 
import sys, os
from osgeo.gdalconst import GA_ReadOnly
from osgeo.osr import SpatialReference
from math import ceil, log10
from optparse import OptionParser
import operator
import sqlite3

tilesize = 256
tileformat = 'png'

tempdriver = gdal.GetDriverByName('MEM')
tiledriver = gdal.GetDriverByName(tileformat)

def writemb(index, data, dxsize, dysize, bands, mb_db):
    """
    Write raster 'data' (of the size 'dataxsize' x 'dataysize') read from
    'dataset' into the mbtiles document 'mb_db' with size 'tilesize' pixels.
    Later this should be replaced by new <TMS Tile Raster Driver> from GDAL.
    """
    if bands == 3 and tileformat == 'png':
        tmp = tempdriver.Create('', tilesize, tilesize, bands=4)
        alpha = tmp.GetRasterBand(4)
        #from Numeric import zeros
        alphaarray = (zeros((dysize, dxsize)) + 255).astype('b')
        alpha.WriteArray( alphaarray, 0, tilesize-dysize )
    else:
        tmp = tempdriver.Create('', tilesize, tilesize, bands=bands)

    tmp.WriteRaster(0, tilesize-dysize, dxsize, dysize, data, band_list=range(1, bands+1))
    tiledriver.CreateCopy('tmp.png', tmp, strict=0)
    query = """insert into tiles 
        (zoom_level, tile_column, tile_row, tile_data) 
        values (%d, %d, %d, ?)""" % (index[0], index[1], index[2])
    cur = mb_db.cursor()
    d = open('tmp.png', 'rb').read()
    cur.execute(query, (sqlite3.Binary(d),))
    cur.close()
    return 0

def init_db(db_filename, metadata):
    if os.path.isfile(db_filename):
        raise Exception('Output file already exists')
    mb_db = sqlite3.connect(db_filename)
    # mb_db.text_factory = str
    mb_db.execute("""
      CREATE TABLE tiles (
        zoom_level integer, 
        tile_column integer, 
        tile_row integer, 
        tile_data blob);
    """)
    
    mb_db.execute("""
      CREATE UNIQUE INDEX tile_index on tiles 
        (zoom_level, tile_column, tile_row);
    """)
    mb_db.execute("""
      CREATE TABLE "metadata" (
        "name" TEXT ,
        "value" TEXT );
    """)
    mb_db.execute("""
      CREATE UNIQUE INDEX "name" ON "metadata" 
        ("name");
    """)
    mb_db.executemany("""
      INSERT INTO metadata (name, value) values
      (?, ?)""", metadata)
    mb_db.commit()
    return mb_db

if __name__ == '__main__':
    parser = OptionParser("%prog usage: %prog [input_file] [output_file]")
    parser.add_option('-n', '--name', dest='name', help='Name')
    parser.add_option('-d', '--description', dest='description', help='Description')
    parser.add_option('-v', '--verbose', dest='verbose', help='Verbose', action='store_true')
    parser.add_option('-r', '--version', dest='version', help='Version', default='1.0')
    parser.add_option('-o', '--overlay', action='store_true',
        dest='overlay', default=False, help='Overlay')

    (options, args) = parser.parse_args()

    try:
        input_file = args[0]
        db_filename = args[1]
    except IndexError, e:
        raise Exception('Input and Output file arguments are required')

    profile = 'local' # later there should be support for TMS global profiles

    isepsg4326 = False
    gdal.AllRegister()

    # Set correct default values.
    if not options.name:
        options.name = os.path.basename(input_file)

    # print "----------\n",options.name           # name of tiff file
    # print options.version                       # 1.0 default in parser
    # print options.description,"----------\n"    # None

    dataset = gdal.Open(input_file, GA_ReadOnly)
    if dataset is None:
        parser.usage()
        
    bands = dataset.RasterCount
    if bands > 3:
        bands = 3
    if bands == 3 and tileformat == 'png':
        from numpy import zeros
    xsize = dataset.RasterXSize
    ysize = dataset.RasterYSize

    geotransform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()

    # (31.533709086005583, 31.414944125572063, 34.786912277506254, 34.61061229179585)

    # LOW LEFT 34.6106123, 31.4149441
    #           west        south
    # UPPER RIGHT 34.7869123, 31.5337091
    #              east        north
    
    north = geotransform[3]
    south = geotransform[3] + geotransform[5] * ysize
    east  = geotransform[0] + geotransform[1] * xsize
    west  = geotransform[0]

    print west, south, east, north
    bounds = "{0},{1},{2},{3}".format(west, south, east, north)

    if options.verbose:
        print "Input (%s):" % input_file
        print "="*80
        print "  Driver:", dataset.GetDriver().ShortName,'/', dataset.GetDriver().LongName
        print "  Size:", xsize, 'x', ysize, 'x', bands
        print "  Projection:", projection
        print "  NSEW: ", (north, south, east, west) 

    if projection and projection.endswith('AUTHORITY["EPSG","4326"]]'):
        isepsg4326 = True
        if options.verbose:
            print "Projection detected as EPSG:4326"

    # Python 2.2 compatibility.
    log2 = lambda x: log10(x) / log10(2) # log2 (base 2 logarithm)
    sum = lambda seq, start=0: reduce(operator.add, seq, start)

    # Zoom levels of the pyramid.
    # Zoom 11-17
    maxzoom = int(max(ceil(log2(xsize/float(tilesize))), ceil(log2(ysize/float(tilesize)))))
    zoompixels = [geotransform[1] * 2.0**(maxzoom-zoom) for zoom in range(0, maxzoom+1)]
    tilecount = sum([
        int(ceil(xsize / (2.0**(maxzoom-zoom)*tilesize))) * \
        int(ceil(ysize / (2.0**(maxzoom-zoom)*tilesize))) \
        for zoom in range(maxzoom+1)
    ])

    if options.verbose:
        print "Output (%s):" % db_filename
        print "="*80
        print "  Format of tiles:", tiledriver.ShortName, '/', tiledriver.LongName
        print "  Size of a tile:", tilesize, 'x', tilesize, 'pixels'
        print "  Count of tiles:", tilecount
        print "  Zoom levels of the pyramid:", maxzoom
        print "  Pixel resolution by zoomlevels:", zoompixels

    tileno = 0
    progress = 0

    layer_type = "overlay" if options.overlay else "baselayer"

    print "Connecting to database %s" % db_filename
    mb_db = init_db(db_filename, 
        [('name', options.name),
        ('version', options.version),
        ('maxzoom', maxzoom),
        ('minzoom', 0),
        ('format', tileformat),
        ('description', options.description),
        ('type', layer_type),
        ('bounds', bounds)])

    for zoom in range(maxzoom, -1, -1):
        # Maximal size of read window in pixels.
        rmaxsize = 2.0**(maxzoom-zoom)*tilesize

        if options.verbose:
            print "-"*80
            print "Zoom %s - pixel %.20f" % (zoom, zoompixels[zoom]), int(2.0**zoom*tilesize)
            print "-"*80

        for ix in range(0, int(ceil( xsize / rmaxsize))):
            # Read window xsize in pixels.
            if ix+1 == int(ceil(xsize / rmaxsize)) and xsize % rmaxsize != 0:
                rxsize = int(xsize % rmaxsize)
            else:
                rxsize = int(rmaxsize)
            
            # Read window left coordinate in pixels.
            rx = int(ix * rmaxsize)

            for iy in range(0, int(ceil(ysize / rmaxsize))):
                # Read window ysize in pixels.
                if iy+1 == int(ceil(ysize / rmaxsize)) and ysize % rmaxsize != 0:
                    rysize = int(ysize % rmaxsize)
                else:
                    rysize = int(rmaxsize)

                # Read window top coordinate in pixels.
                ry = int(ysize - (iy * rmaxsize)) - rysize
                dxsize = int(rxsize/rmaxsize * tilesize)
                dysize = int(rysize/rmaxsize * tilesize)
                
                # Show the progress bar.
                percent = int(ceil((tileno) / float(tilecount-1) * 100))
                while progress <= percent:
                    if progress % 10 == 0:
                        sys.stdout.write( "%d" % progress )
                        sys.stdout.flush()
                    else:
                        sys.stdout.write( '.' )
                        sys.stdout.flush()
                    progress += 2.5
               
                # Load raster from read window.
                data = dataset.ReadRaster(rx, ry, rxsize, rysize, dxsize, dysize)
                writemb((zoom, ix, iy), data, dxsize, dysize, bands, mb_db)
                if tileno % 1000 == 0:
                    mb_db.commit()
                tileno += 1

    mb_db.commit()
    mb_db.close()
    # Last \n for the progress bar
    print "\nDone creating .mbtiles file. You can now drop this file into a"
    print "Maps on a Stick 'Maps' folder or MapBox on iPad folder"