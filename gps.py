#!/usr/bin/env python

"""
Created on Sat Nov 28 12:51:07 2015

@author: tracek
"""

from __future__ import division
import exifread
from datetime import datetime
from geopy.geocoders import Nominatim

class GPSLocator(object):

    def __init__(self):
        self.geolocator = Nominatim()

    def _convert_to_deg(self, value):
        degrees = value[0].num / value[0].den
        minutes = value[1].num / value[1].den
        seconds = value[2].num / value[2].den
        return degrees + minutes / 60.0 + seconds / 3600.0

    def get_gps_metadata(self, filepath):
        result = {}

        try:
            f = open(filepath, 'rb')
            tags = exifread.process_file(f)
            GPSDate = tags['GPS GPSDate'].values
            date = datetime.strptime(GPSDate, '%Y:%m:%d')

            GPSAltitude = tags['GPS GPSAltitude'].values
            altitude = eval(str(GPSAltitude[0]))

            GPSLatitude = tags['GPS GPSLatitude'].values
            GPSLatitudeRef = tags['GPS GPSLatitudeRef'].values
            latitude = self._convert_to_deg(GPSLatitude) if GPSLatitudeRef == 'N' else -self._convert_to_deg(GPSLatitude)

            GPSLongitude = tags['GPS GPSLongitude'].values
            GPSLongitudeRef = tags['GPS GPSLongitudeRef'].values
            longitude = self._convert_to_deg(GPSLongitude) if GPSLongitudeRef == 'E' else -self._convert_to_deg(GPSLongitude)

            GPSMapDatum = tags['GPS GPSMapDatum'].values

            result['coordinates'] = (latitude, longitude)
            result['altitude'] = altitude
            result['location'] = self.geolocator.reverse((latitude, longitude)).address
            result['datum'] = GPSMapDatum
            result['date'] = str(date.date())
        except:
            result['coordinates'] = 'Unknown'
            result['altitude'] = 'Unknown'
            result['location'] = 'Unknown'
            result['datum'] = 'Unknown'
            result['date'] = 'Unknown'
            raise

        return result

if __name__ == '__main__':
    locator = GPSLocator()
    metadata = locator.get_gps_metadata('/home/tracek/Notebooks/data/27302080E.jpg')
    print metadata
